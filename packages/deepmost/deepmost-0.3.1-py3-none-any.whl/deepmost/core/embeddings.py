"""Embedding providers for different backends with full LLM-derived metrics"""

import numpy as np
import torch
import logging
from typing import List, Dict, Optional, Protocol
from transformers import AutoTokenizer, AutoModel
import re
import json
import os
import random

logger = logging.getLogger(__name__)

class EmbeddingProvider(Protocol):
    """Protocol for embedding providers"""

    def get_embedding(self, text: str, turn_number: int) -> np.ndarray:
        """Get embedding for text"""
        ...

    def analyze_metrics(self, history: List[Dict[str, str]], turn_number: int) -> Dict[str, float]:
        """Analyze conversation metrics"""
        ...

    def generate_response(
        self,
        history: List[Dict[str, str]],
        user_input: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate response (optional method)"""
        return "Thank you for your message. Could you tell me more?"


class OpenSourceEmbeddings:
    """Open-source embedding provider using HuggingFace models and LLM for ALL metrics analysis."""

    def __init__(
        self,
        model_name: str,
        device: torch.device,
        expected_dim: int,
        llm_model: Optional[str] = None
    ):
        self.device = device
        self.expected_dim = expected_dim
        self.MAX_TURNS_REFERENCE = 20

        logger.info(f"Loading embedding model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device)
        self.native_dim = self.model.config.hidden_size
        logger.info(f"Embedding model loaded. Native dim: {self.native_dim}, Expected dim: {self.expected_dim}")

        self.llm = None
        if llm_model:
            logger.info(f"Attempting to load GGUF LLM: {llm_model}")
            try:
                from llama_cpp import Llama
                
                llama_params = {
                    "n_gpu_layers": -1 if device.type == 'cuda' else 0,
                    "n_ctx": 8192,
                    "verbose": False 
                }

                if "/" in llm_model and not llm_model.lower().endswith(".gguf"):
                    repo_id = llm_model
                    logger.info(f"LLM '{repo_id}' is a HuggingFace repo. Using Llama.from_pretrained.")
                    
                    gguf_filename_pattern = "*Q4_K_M.gguf"
                    
                    try:
                        self.llm = Llama.from_pretrained(
                            repo_id=repo_id,
                            filename=gguf_filename_pattern, 
                            local_dir_use_symlinks=False, 
                            **llama_params
                        )
                        logger.info(f"LLM loaded successfully from HuggingFace repo '{repo_id}'.")

                    except Exception as e_from_pretrained:
                        logger.warning(f"Llama.from_pretrained failed for '{repo_id}' (pattern: '{gguf_filename_pattern}'): {e_from_pretrained}. "
                                       f"Ensure repo has a matching GGUF or try filename=None.")
                        raise 

                elif llm_model.lower().endswith(".gguf"): 
                    if not os.path.exists(llm_model):
                        logger.error(f"Local GGUF file not found: {llm_model}")
                        raise FileNotFoundError(f"Local GGUF file not found: {llm_model}")
                    logger.info(f"Loading LLM from local GGUF path: {llm_model}")
                    self.llm = Llama(model_path=llm_model, **llama_params)
                    logger.info(f"LLM loaded successfully from local path: {llm_model}")
                else:
                    logger.warning(f"LLM path '{llm_model}' not recognized as HF repo ID or local .gguf file. LLM not loaded.")
            
            except ImportError:
                logger.warning("llama-cpp-python is not installed. LLM features will be unavailable.")
            except FileNotFoundError as e: 
                logger.error(e)
                self.llm = None
            except Exception as e:
                logger.warning(f"Failed to load GGUF LLM '{llm_model}': {e}. LLM features may be unavailable.")
                self.llm = None
        
        if not self.llm:
            logger.error(
                "No LLM loaded. ALL metrics require LLM analysis for this system. "
                "Please provide a valid LLM model for full functionality."
            )
            raise ValueError("LLM model is required for all metrics analysis. Please provide llm_model parameter.")

    def get_embedding(self, text: str, turn_number: int) -> np.ndarray:
        inputs = self.tokenizer(
            text, padding=True, truncation=True, return_tensors='pt', max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state
            attention_mask = inputs['attention_mask']
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
            sum_embeddings = torch.sum(embeddings * input_mask_expanded, 1)
            sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            mean_embeddings = sum_embeddings / sum_mask
            normalized = torch.nn.functional.normalize(mean_embeddings, p=2, dim=1)
            embedding_native = normalized.cpu().numpy()[0]

        if embedding_native.shape[0] == self.expected_dim:
            embedding = embedding_native
        elif embedding_native.shape[0] > self.expected_dim:
            embedding = embedding_native[:self.expected_dim]
        else: 
            embedding = np.zeros(self.expected_dim, dtype=np.float32)
            embedding[:embedding_native.shape[0]] = embedding_native

        progress = min(1.0, turn_number / self.MAX_TURNS_REFERENCE)
        scaled_embedding = embedding * (0.6 + 0.4 * progress)
        return scaled_embedding.astype(np.float32)

    def _get_all_metrics_from_llm(self, history: List[Dict[str, str]], turn_number: int) -> Dict:
        """Get ALL metrics (core + derived) from LLM via comprehensive JSON analysis."""
        if not self.llm:
            logger.error("LLM is required for all metrics analysis but not available.")
            raise ValueError("LLM model is required for metrics analysis.")
        
        conversation_text = "\n".join([f"{msg['speaker'].capitalize()}: {msg['message']}" for msg in history])
        
        if not conversation_text.strip():
            logger.warning("Conversation history is empty for LLM comprehensive analysis.")
            return self._get_emergency_fallback_metrics(history, turn_number)

        # Comprehensive prompt for ALL metrics (core + derived)
        prompt = f"""Analyze the following sales conversation and provide a comprehensive analysis in JSON format.

CONVERSATION:
---
{conversation_text}
---

Provide a detailed analysis covering ALL aspects below. Respond ONLY with valid JSON containing these exact keys:

{{
  "customer_engagement": 0.0-1.0,
  "sales_effectiveness": 0.0-1.0,
  "conversation_length": number,
  "outcome": 0.0-1.0,
  "progress": 0.0-1.0,
  "conversation_style": "string",
  "conversation_flow": "string", 
  "communication_channel": "string",
  "primary_customer_needs": ["list", "of", "needs"],
  "engagement_trend": 0.0-1.0,
  "objection_count": 0.0-1.0,
  "value_proposition_mentions": 0.0-1.0,
  "technical_depth": 0.0-1.0,
  "urgency_level": 0.0-1.0,
  "competitive_context": 0.0-1.0,
  "pricing_sensitivity": 0.0-1.0,
  "decision_authority_signals": 0.0-1.0
}}

DETAILED SCORING GUIDELINES:

**CORE METRICS (Required for PPO model):**

**customer_engagement** (0.0-1.0): How engaged and interested the customer appears
- 0.0-0.2: Completely disengaged, very short responses, no interest, dismissive
- 0.3-0.4: Low engagement, minimal responses, seems distracted or uninterested
- 0.5-0.6: Moderate engagement, participating normally, some interest shown
- 0.7-0.8: High engagement, asking questions, showing clear interest, interactive
- 0.9-1.0: Extremely engaged, ready to buy, making decisions, highly enthusiastic

**sales_effectiveness** (0.0-1.0): How effective the sales representative's approach is
- 0.0-0.2: Very poor approach, pushing away customer, unprofessional, harmful
- 0.3-0.4: Poor approach, not addressing needs, unclear responses, missing opportunities
- 0.5-0.6: Adequate approach, some value shown, decent communication, basic competence
- 0.7-0.8: Good approach, addressing needs well, building value, professional
- 0.9-1.0: Excellent approach, perfectly addressing needs, very professional, masterful

**conversation_length** (number): Exact count of messages/turns in the conversation (count the actual messages)

**outcome** (0.0-1.0): Likelihood that this conversation will result in a sale/conversion
- 0.0-0.2: Very unlikely to convert, customer rejecting, strong negative signals
- 0.3-0.4: Unlikely to convert, significant objections, lukewarm interest
- 0.5-0.6: Moderate chance, some interest but concerns remain, neutral positioning
- 0.7-0.8: Likely to convert, strong interest, moving toward decision
- 0.9-1.0: Very likely to convert, customer ready to buy, commitment signals

**progress** (0.0-1.0): How far along the sales process this conversation represents
- 0.0-0.2: Initial contact, problem identification stage
- 0.3-0.4: Need discovery, solution exploration stage  
- 0.5-0.6: Solution presentation, value demonstration stage
- 0.7-0.8: Negotiation, objection handling, final considerations stage
- 0.9-1.0: Closing, decision making, commitment stage

**CONVERSATION CHARACTERISTICS:**

**conversation_style** (string): Choose the most fitting style:
"casual_friendly", "direct_professional", "technical_detailed", "consultative_advisory", 
"empathetic_supportive", "skeptical_challenging", "urgent_time_pressed", "confused_overwhelmed", 
"knowledgeable_assertive", "storytelling_narrative"

**conversation_flow** (string): Choose the most fitting flow pattern:
"standard_linear", "multiple_objection_loops", "subject_switching", "interrupted_followup", 
"technical_deep_dive", "competitive_comparison", "gradual_discovery", "immediate_interest", 
"initial_rejection", "stakeholder_expansion", "pricing_negotiation", "implementation_concerns", 
"value_justification", "relationship_building", "multi_session", "demo_walkthrough"

**communication_channel** (string): Choose the most likely channel:
"email", "live_chat", "phone_call", "video_call", "in_person", "sms", "social_media"

**primary_customer_needs** (array): Select 2-3 most relevant needs:
"efficiency", "cost_reduction", "growth", "compliance", "integration", "usability", 
"reliability", "security", "support", "analytics"

**BEHAVIORAL ANALYTICS:**

**engagement_trend** (0.0-1.0): Is customer engagement increasing or decreasing?
- 0.0-0.3: Strongly declining engagement throughout conversation
- 0.4-0.6: Stable or slightly changing engagement  
- 0.7-1.0: Increasing engagement throughout conversation

**objection_count** (0.0-1.0): Level of customer objections/resistance normalized
- 0.0: No objections raised
- 0.5: Moderate objections (price, features, timing)
- 1.0: Strong/multiple objections (not interested, won't work, too expensive)

**value_proposition_mentions** (0.0-1.0): How well sales rep articulated value
- 0.0: No value mentioned or demonstrated
- 0.5: Some benefits mentioned, moderate value presentation
- 1.0: Strong, clear, compelling value propositions presented

**technical_depth** (0.0-1.0): How technical/detailed the conversation is
- 0.0: Basic, non-technical discussion, high-level only
- 0.5: Some technical terms or concepts, moderate detail
- 1.0: Highly technical, detailed technical discussion, deep dive

**urgency_level** (0.0-1.0): Time pressure or urgency indicators
- 0.0: No urgency mentioned, relaxed timeline
- 0.5: Some time considerations, moderate urgency
- 1.0: High urgency, deadlines, time-sensitive decisions

**competitive_context** (0.0-1.0): Mentions of competitors or alternatives
- 0.0: No competitive mentions or comparisons
- 0.5: Some comparison or alternatives discussed
- 1.0: Heavy competitive comparison focus, detailed competitive analysis

**pricing_sensitivity** (0.0-1.0): Customer's focus on cost/budget
- 0.0: Price not discussed or not a concern
- 0.5: Some price discussion or budget considerations
- 1.0: Heavy focus on price, budget constraints, cost concerns

**decision_authority_signals** (0.0-1.0): Customer's decision-making power
- 0.0-0.3: Low authority ("need to check with boss", "team decision", "not my call")
- 0.4-0.6: Moderate authority (some input but not final decision)
- 0.7-1.0: High authority ("I decide", "my budget", "I approve", "I can sign off")

CRITICAL REQUIREMENTS:
1. Respond with ONLY the JSON object, no explanations or additional text
2. All numeric values must be between 0.0 and 1.0 (except conversation_length which is a count)
3. String values must match exactly the options provided
4. Primary_customer_needs must be an array with 2-3 items from the specified list
5. Base your analysis on the actual conversation content, not assumptions

JSON Response:"""

        try:
            llm_response = self.llm(
                prompt,
                max_tokens=400,
                temperature=0.1,
                stop=["\n\n", "```"],
            )
            raw_llm_output = llm_response['choices'][0]['text'].strip()
            logger.debug(f"DEBUG: LLM Raw Output for all metrics: '{raw_llm_output}'")

            # Parse the JSON
            json_match = re.search(r"\{.*\}", raw_llm_output, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                try:
                    parsed_json = json.loads(json_str)
                    
                    # Validate and normalize the JSON response
                    validated_metrics = self._validate_and_normalize_all_metrics(parsed_json, history, turn_number)
                    logger.info(f"Successfully parsed ALL LLM metrics with {len(validated_metrics)} fields")
                    return validated_metrics
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to decode JSON from LLM output: '{json_str}'. Error: {e}")
            else:
                logger.warning(f"No JSON object found in LLM output: '{raw_llm_output}'")
        
        except Exception as e:
            logger.error(f"LLM comprehensive metrics analysis failed: {e}", exc_info=True)
        
        # If LLM fails, we still need to return something, but log it as an error
        logger.error("LLM analysis failed. Using emergency fallback - this should not happen in production.")
        return self._get_emergency_fallback_metrics(history, turn_number)

    def _validate_and_normalize_all_metrics(self, parsed_json: Dict, history: List[Dict[str, str]], turn_number: int) -> Dict:
        """Validate and normalize ALL LLM-provided metrics (core + derived)."""
        validated = {}
        
        # CORE METRICS (required for PPO model)
        core_numeric_fields = [
            'customer_engagement', 'sales_effectiveness', 'outcome', 'progress'
        ]
        
        for field in core_numeric_fields:
            value = parsed_json.get(field, 0.5)
            if isinstance(value, (int, float)):
                validated[field] = float(np.clip(value, 0.0, 1.0))
            else:
                logger.warning(f"Invalid {field} value: {value}, using 0.5")
                validated[field] = 0.5
        
        # Conversation length (special core metric - should be actual count)
        conv_length = parsed_json.get('conversation_length', len(history))
        if isinstance(conv_length, (int, float)) and conv_length >= 0:
            validated['conversation_length'] = float(conv_length)
        else:
            validated['conversation_length'] = float(len(history))
        
        # DERIVED BEHAVIORAL METRICS (all numeric 0.0-1.0)
        derived_numeric_fields = [
            'engagement_trend', 'objection_count', 'value_proposition_mentions', 
            'technical_depth', 'urgency_level', 'competitive_context', 
            'pricing_sensitivity', 'decision_authority_signals'
        ]
        
        for field in derived_numeric_fields:
            value = parsed_json.get(field, 0.5)
            if isinstance(value, (int, float)):
                validated[field] = float(np.clip(value, 0.0, 1.0))
            else:
                logger.warning(f"Invalid {field} value: {value}, using 0.5")
                validated[field] = 0.5
        
        # STRING CATEGORICAL FIELDS
        style_options = [
            "casual_friendly", "direct_professional", "technical_detailed", "consultative_advisory",
            "empathetic_supportive", "skeptical_challenging", "urgent_time_pressed", "confused_overwhelmed",
            "knowledgeable_assertive", "storytelling_narrative"
        ]
        validated['conversation_style'] = parsed_json.get('conversation_style', 'direct_professional')
        if validated['conversation_style'] not in style_options:
            logger.warning(f"Invalid conversation_style: {validated['conversation_style']}, using default")
            validated['conversation_style'] = 'direct_professional'
        
        flow_options = [
            "standard_linear", "multiple_objection_loops", "subject_switching", "interrupted_followup",
            "technical_deep_dive", "competitive_comparison", "gradual_discovery", "immediate_interest",
            "initial_rejection", "stakeholder_expansion", "pricing_negotiation", "implementation_concerns",
            "value_justification", "relationship_building", "multi_session", "demo_walkthrough"
        ]
        validated['conversation_flow'] = parsed_json.get('conversation_flow', 'standard_linear')
        if validated['conversation_flow'] not in flow_options:
            logger.warning(f"Invalid conversation_flow: {validated['conversation_flow']}, using default")
            validated['conversation_flow'] = 'standard_linear'
        
        channel_options = ["email", "live_chat", "phone_call", "video_call", "in_person", "sms", "social_media"]
        validated['communication_channel'] = parsed_json.get('communication_channel', 'email')
        if validated['communication_channel'] not in channel_options:
            logger.warning(f"Invalid communication_channel: {validated['communication_channel']}, using default")
            validated['communication_channel'] = 'email'
        
        # ARRAY FIELD for customer needs
        need_options = [
            "efficiency", "cost_reduction", "growth", "compliance", "integration",
            "usability", "reliability", "security", "support", "analytics"
        ]
        needs = parsed_json.get('primary_customer_needs', ['efficiency', 'cost_reduction'])
        if isinstance(needs, list):
            validated['primary_customer_needs'] = [need for need in needs if need in need_options][:3]
        else:
            logger.warning(f"Invalid primary_customer_needs: {needs}, using default")
            validated['primary_customer_needs'] = ['efficiency', 'cost_reduction']
        
        if not validated['primary_customer_needs']:
            validated['primary_customer_needs'] = ['efficiency', 'cost_reduction']
        
        return validated

    def _get_emergency_fallback_metrics(self, history: List[Dict[str, str]], turn_number: int) -> Dict:
        """Emergency fallback when LLM completely fails - should rarely be used."""
        logger.error("Using emergency fallback metrics - this indicates a system failure")
        
        # Minimal analysis based on conversation length and basic text patterns
        conversation_length = len(history)
        customer_text = " ".join([msg['message'].lower() for msg in history if msg['speaker'] == 'customer'])
        
        # Very basic pattern matching for emergency fallback only
        has_positive_signals = any(signal in customer_text for signal in ['interested', 'yes', 'sounds good', 'tell me more'])
        has_negative_signals = any(signal in customer_text for signal in ['not interested', 'no', 'expensive', 'too much'])
        
        base_engagement = 0.6 if has_positive_signals else 0.3 if has_negative_signals else 0.4
        base_outcome = 0.7 if has_positive_signals else 0.2 if has_negative_signals else 0.4
        
        return {
            # Core metrics
            'customer_engagement': base_engagement,
            'sales_effectiveness': 0.5,  # Neutral since we can't assess without LLM
            'conversation_length': float(conversation_length),
            'outcome': base_outcome,
            'progress': min(1.0, turn_number / self.MAX_TURNS_REFERENCE),
            
            # Derived categorical metrics
            'conversation_style': 'direct_professional',
            'conversation_flow': 'standard_linear',
            'communication_channel': 'email',
            'primary_customer_needs': ['efficiency', 'cost_reduction'],
            
            # Derived behavioral metrics
            'engagement_trend': 0.5,
            'objection_count': 0.4 if has_negative_signals else 0.2,
            'value_proposition_mentions': 0.3,
            'technical_depth': 0.3,
            'urgency_level': 0.2,
            'competitive_context': 0.1,
            'pricing_sensitivity': 0.5 if 'price' in customer_text or 'cost' in customer_text else 0.3,
            'decision_authority_signals': 0.5
        }

    def _generate_probability_trajectory(self, history: List[Dict[str, str]], all_metrics: Dict) -> Dict[int, float]:
        """Generate realistic probability trajectory using comprehensive LLM metrics."""
        trajectory = {}
        num_turns = len(history)
        
        if num_turns == 0:
            return {0: 0.5}
        
        # Use LLM-derived metrics for trajectory generation
        engagement = all_metrics.get('customer_engagement', 0.5)
        effectiveness = all_metrics.get('sales_effectiveness', 0.5)
        engagement_trend = all_metrics.get('engagement_trend', 0.5)
        objection_count = all_metrics.get('objection_count', 0.3)
        outcome = all_metrics.get('outcome', 0.5)
        
        # Sophisticated trajectory calculation based on LLM metrics
        base_prob = 0.2
        trend_factor = (engagement * 0.4 + effectiveness * 0.3 + engagement_trend * 0.3)
        
        # Adjust for objections
        objection_penalty = objection_count * 0.25
        
        for i in range(num_turns):
            progress = i / max(1, num_turns - 1)
            
            # Calculate probability with sophisticated weighting
            prob = base_prob + (trend_factor - objection_penalty - 0.3) * progress * 1.5
            
            # Apply engagement trend
            if engagement_trend > 0.7:
                prob += progress * 0.25  # Increasing engagement boosts trajectory
            elif engagement_trend < 0.3:
                prob -= progress * 0.2   # Decreasing engagement hurts trajectory
            
            # Ensure trajectory moves toward the final outcome
            target_prob = outcome
            prob = prob * (1 - progress * 0.3) + target_prob * (progress * 0.3)
            
            # Smooth progression with some realistic variation
            if i > 0:
                prev_prob = trajectory[i-1]
                max_change = 0.15
                prob = max(prev_prob - max_change, min(prev_prob + max_change, prob))
            
            # Add small realistic noise
            noise = random.uniform(-0.015, 0.015)
            prob = np.clip(prob + noise, 0.05, 0.95)
            
            trajectory[i] = round(prob, 4)
        
        return trajectory

    def analyze_metrics(self, history: List[Dict[str, str]], turn_number: int) -> Dict[str, float]:
        """Analyze conversation metrics using LLM for ALL metrics."""
        
        # Get ALL metrics from LLM (core + derived)
        all_metrics = self._get_all_metrics_from_llm(history, turn_number)
        
        # Generate sophisticated probability trajectory
        probability_trajectory = self._generate_probability_trajectory(history, all_metrics)
        
        # Add the probability trajectory to the metrics
        all_metrics['probability_trajectory'] = probability_trajectory
        
        llm_derived = self.llm is not None
        logger.info(f"Full LLM Metrics Analysis (LLM available: {llm_derived}) - "
                   f"Engagement: {all_metrics['customer_engagement']:.2f}, "
                   f"Effectiveness: {all_metrics['sales_effectiveness']:.2f}, "
                   f"Outcome: {all_metrics['outcome']:.2f}, "
                   f"Style: {all_metrics['conversation_style']}, "
                   f"Flow: {all_metrics['conversation_flow']}")
        
        return all_metrics

    def generate_response(
        self,
        history: List[Dict[str, str]],
        user_input: str,
        system_prompt: Optional[str] = None
    ) -> str:
        if not self.llm:
            logger.warning("LLM not available for response generation. Returning canned response.")
            return "Thank you for your message. Could you provide more details?"

        messages_for_llm = []
        if system_prompt:
            messages_for_llm.append({"role": "system", "content": system_prompt})

        for msg in history:
            role = "user" if msg['speaker'] == 'customer' else "assistant"
            messages_for_llm.append({"role": role, "content": msg['message']})
        
        messages_for_llm.append({"role": "user", "content": user_input})
        
        try:
            logger.debug(f"LLM prompt messages for response generation: {messages_for_llm}")
            chat_completion = self.llm.create_chat_completion(
                messages=messages_for_llm,
                max_tokens=150,
                temperature=0.7,
                stop=["\nUser:", "\nCustomer:", "\n<|user|>", "\n<|end|>"] 
            )
            generated_text = chat_completion['choices'][0]['message']['content'].strip()
            logger.info(f"LLM generated response: {generated_text}")
            return generated_text
        except Exception as e:
            logger.error(f"LLM response generation failed: {e}", exc_info=True)
            return "I understand. Could you please provide more details about what you're looking for?"


class AzureEmbeddings:
    """Azure OpenAI embedding provider with LLM-derived metrics (requires Azure OpenAI chat model)."""

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        deployment: str, 
        api_version: str, 
        expected_dim: int,
        chat_deployment: Optional[str] = None
    ):
        from openai import AzureOpenAI 

        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version
        )
        self.deployment_name = deployment 
        self.chat_deployment = chat_deployment  # For metrics analysis
        self.expected_dim = expected_dim
        self.native_dim = 0 
        self.MAX_TURNS_REFERENCE = 20

        try:
            logger.info(f"Testing Azure OpenAI connection with embedding deployment: {self.deployment_name}")
            test_response = self.client.embeddings.create(
                input="test",
                model=self.deployment_name
            )
            self.native_dim = len(test_response.data[0].embedding)
            logger.info(f"Azure embeddings initialized. Native dim: {self.native_dim}, Expected dim: {self.expected_dim}")
        except Exception as e:
            logger.error(f"Failed to initialize Azure embeddings (model: {self.deployment_name}): {e}")
            raise

        # Check if chat model is available for LLM metrics
        if not self.chat_deployment:
            logger.warning(
                "No Azure chat deployment provided. Metrics analysis will use basic fallbacks. "
                "For full LLM-derived metrics, provide chat_deployment parameter."
            )

    def get_embedding(self, text: str, turn_number: int) -> np.ndarray:
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.deployment_name
            )
            embedding_native = np.array(response.data[0].embedding, dtype=np.float32)
        except Exception as e:
            logger.error(f"Azure embedding API call failed: {e}")
            dim_to_use = self.native_dim if self.native_dim > 0 else self.expected_dim
            embedding_native = np.zeros(dim_to_use, dtype=np.float32)

        if self.native_dim == 0 and embedding_native.shape[0] > 0 : 
             self.native_dim = embedding_native.shape[0]

        if embedding_native.shape[0] == self.expected_dim:
            embedding = embedding_native
        elif embedding_native.shape[0] > self.expected_dim:
            embedding = embedding_native[:self.expected_dim] 
        else: 
            embedding = np.zeros(self.expected_dim, dtype=np.float32)
            embedding[:embedding_native.shape[0]] = embedding_native 

        progress = min(1.0, turn_number / self.MAX_TURNS_REFERENCE)
        scaled_embedding = embedding * (0.6 + 0.4 * progress)
        return scaled_embedding.astype(np.float32)

    def _get_all_metrics_from_azure_llm(self, history: List[Dict[str, str]], turn_number: int) -> Dict:
        """Get ALL metrics from Azure OpenAI chat model."""
        if not self.chat_deployment:
            logger.warning("No Azure chat deployment available. Using fallback metrics.")
            return self._get_azure_fallback_metrics(history, turn_number)
        
        conversation_text = "\n".join([f"{msg['speaker'].capitalize()}: {msg['message']}" for msg in history])
        
        if not conversation_text.strip():
            logger.warning("Conversation history is empty for Azure LLM analysis.")
            return self._get_azure_fallback_metrics(history, turn_number)

        # Same comprehensive prompt as OpenSource implementation
        messages = [
            {
                "role": "system",
                "content": "You are an expert sales conversation analyst. Provide comprehensive metrics analysis in JSON format only."
            },
            {
                "role": "user",
                "content": f"""Analyze this sales conversation and provide ALL metrics in JSON format.

CONVERSATION:
---
{conversation_text}
---

Respond with ONLY valid JSON containing these exact keys:

{{
  "customer_engagement": 0.0-1.0,
  "sales_effectiveness": 0.0-1.0,
  "conversation_length": {len(history)},
  "outcome": 0.0-1.0,
  "progress": 0.0-1.0,
  "conversation_style": "direct_professional",
  "conversation_flow": "standard_linear", 
  "communication_channel": "email",
  "primary_customer_needs": ["efficiency", "cost_reduction"],
  "engagement_trend": 0.0-1.0,
  "objection_count": 0.0-1.0,
  "value_proposition_mentions": 0.0-1.0,
  "technical_depth": 0.0-1.0,
  "urgency_level": 0.0-1.0,
  "competitive_context": 0.0-1.0,
  "pricing_sensitivity": 0.0-1.0,
  "decision_authority_signals": 0.0-1.0
}}

Use the same detailed scoring guidelines as the comprehensive analysis system. Return ONLY the JSON object."""
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.chat_deployment,
                messages=messages,
                max_tokens=400,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up JSON response
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed_json = json.loads(json_str)
                
                # Use same validation as OpenSource
                validated_metrics = self._validate_azure_metrics(parsed_json, history, turn_number)
                logger.info(f"Successfully parsed Azure LLM metrics with {len(validated_metrics)} fields")
                return validated_metrics
            else:
                logger.warning(f"No JSON found in Azure response: {content}")
        
        except Exception as e:
            logger.error(f"Azure LLM metrics analysis failed: {e}")
        
        return self._get_azure_fallback_metrics(history, turn_number)

    def _validate_azure_metrics(self, parsed_json: Dict, history: List[Dict[str, str]], turn_number: int) -> Dict:
        """Validate Azure LLM metrics using same logic as OpenSource."""
        validated = {}
        
        # Core metrics
        core_fields = ['customer_engagement', 'sales_effectiveness', 'outcome', 'progress']
        for field in core_fields:
            value = parsed_json.get(field, 0.5)
            validated[field] = float(np.clip(value, 0.0, 1.0)) if isinstance(value, (int, float)) else 0.5
        
        validated['conversation_length'] = float(len(history))
        
        # Derived behavioral metrics
        derived_fields = [
            'engagement_trend', 'objection_count', 'value_proposition_mentions',
            'technical_depth', 'urgency_level', 'competitive_context',
            'pricing_sensitivity', 'decision_authority_signals'
        ]
        for field in derived_fields:
            value = parsed_json.get(field, 0.5)
            validated[field] = float(np.clip(value, 0.0, 1.0)) if isinstance(value, (int, float)) else 0.5
        
        # Categorical fields with validation
        validated['conversation_style'] = parsed_json.get('conversation_style', 'direct_professional')
        validated['conversation_flow'] = parsed_json.get('conversation_flow', 'standard_linear')
        validated['communication_channel'] = parsed_json.get('communication_channel', 'email')
        
        needs = parsed_json.get('primary_customer_needs', ['efficiency', 'cost_reduction'])
        validated['primary_customer_needs'] = needs if isinstance(needs, list) else ['efficiency', 'cost_reduction']
        
        return validated

    def _get_azure_fallback_metrics(self, history: List[Dict[str, str]], turn_number: int) -> Dict:
        """Fallback metrics for Azure when LLM is not available."""
        logger.warning("Azure LLM not available. Using basic enhanced metrics.")
        
        conversation_length = float(len(history))
        progress_metric = min(1.0, turn_number / self.MAX_TURNS_REFERENCE)
        
        # Basic content analysis
        customer_text = " ".join([msg['message'].lower() for msg in history if msg['speaker'] == 'customer'])
        
        engagement = 0.5
        effectiveness = 0.5
        outcome = 0.5
        
        # Basic signal detection
        if any(signal in customer_text for signal in ['interested', 'buy', 'purchase', 'yes', 'sounds good']):
            engagement = 0.7
            outcome = 0.7
        if any(obj in customer_text for obj in ['expensive', 'costly', 'not interested', 'no']):
            engagement = 0.3
            outcome = 0.3
        
        return {
            # Core metrics
            'customer_engagement': engagement,
            'sales_effectiveness': effectiveness,
            'conversation_length': conversation_length,
            'outcome': outcome,
            'progress': progress_metric,
            
            # Derived metrics - basic versions
            'conversation_style': 'direct_professional',
            'conversation_flow': 'standard_linear',
            'communication_channel': 'email',
            'primary_customer_needs': ['efficiency', 'cost_reduction'],
            'probability_trajectory': {i: 0.5 for i in range(len(history))},
            
            # Behavioral metrics - basic analysis
            'engagement_trend': 0.5,
            'objection_count': 0.4 if any(obj in customer_text for obj in ['expensive', 'costly', 'no']) else 0.2,
            'value_proposition_mentions': 0.3,
            'technical_depth': 0.4,
            'urgency_level': 0.2,
            'competitive_context': 0.1,
            'pricing_sensitivity': 0.5 if 'price' in customer_text or 'cost' in customer_text else 0.3,
            'decision_authority_signals': 0.5
        }

    def analyze_metrics(self, history: List[Dict[str, str]], turn_number: int) -> Dict[str, float]:
        """Analyze conversation metrics using Azure OpenAI for ALL metrics."""
        
        # Get all metrics from Azure LLM or fallback
        all_metrics = self._get_all_metrics_from_azure_llm(history, turn_number)
        
        # Generate probability trajectory
        probability_trajectory = self._generate_azure_probability_trajectory(history, all_metrics)
        all_metrics['probability_trajectory'] = probability_trajectory
        
        azure_llm_available = self.chat_deployment is not None
        logger.info(f"Azure Metrics Analysis (Chat model available: {azure_llm_available}) - "
                   f"Engagement: {all_metrics['customer_engagement']:.2f}, "
                   f"Effectiveness: {all_metrics['sales_effectiveness']:.2f}, "
                   f"Outcome: {all_metrics['outcome']:.2f}")
        
        return all_metrics

    def _generate_azure_probability_trajectory(self, history: List[Dict[str, str]], all_metrics: Dict) -> Dict[int, float]:
        """Generate probability trajectory for Azure backend."""
        trajectory = {}
        num_turns = len(history)
        
        if num_turns == 0:
            return {0: 0.5}
        
        # Use metrics to generate trajectory
        engagement = all_metrics.get('customer_engagement', 0.5)
        effectiveness = all_metrics.get('sales_effectiveness', 0.5)
        outcome = all_metrics.get('outcome', 0.5)
        
        for i in range(num_turns):
            progress = i / max(1, num_turns - 1)
            
            # Simple trajectory calculation
            base_trend = (engagement + effectiveness) / 2
            prob = 0.3 + (base_trend - 0.5) * progress + (outcome - 0.5) * progress * 0.5
            prob = np.clip(prob, 0.05, 0.95)
            
            trajectory[i] = round(prob, 4)
        
        return trajectory

    def generate_response(
        self,
        history: List[Dict[str, str]],
        user_input: str,
        system_prompt: Optional[str] = None
    ) -> str:
        if not self.chat_deployment:
            logger.warning(
                "Azure chat deployment not available for response generation. "
                "For LLM responses with Azure backend, provide chat_deployment parameter."
            )
            return "Thank you for your inquiry. An agent will follow up with you."
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        for msg in history:
            role = "user" if msg['speaker'] == 'customer' else "assistant"
            messages.append({"role": role, "content": msg['message']})
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model=self.chat_deployment,
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            generated_text = response.choices[0].message.content.strip()
            logger.info(f"Azure LLM generated response: {generated_text}")
            return generated_text
            
        except Exception as e:
            logger.error(f"Azure response generation failed: {e}")
            return "I understand your needs. Let me help you find the right solution."