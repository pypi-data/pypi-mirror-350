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
        self.is_qwen_model = False
        
        if llm_model:
            logger.info(f"Attempting to load GGUF LLM: {llm_model}")
            try:
                from llama_cpp import Llama
                
                # Detect Qwen models for special handling
                self.is_qwen_model = 'qwen' in llm_model.lower()
                if self.is_qwen_model:
                    logger.info("Detected Qwen model - using specialized prompting strategies")
                
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

        # Try model-specific strategies first, then general ones
        if self.is_qwen_model:
            strategies = [
                self._get_qwen_json_strategy_1,
                self._get_qwen_json_strategy_2,
                self._get_qwen_json_strategy_3,
                self._get_json_strategy_1,
                self._get_json_strategy_2
            ]
        else:
            strategies = [
                self._get_json_strategy_1,
                self._get_json_strategy_2, 
                self._get_json_strategy_3
            ]
        
        for i, strategy in enumerate(strategies):
            try:
                result = strategy(conversation_text, turn_number)
                if result:
                    logger.info(f"Successfully got LLM metrics using strategy {i+1}")
                    return result
            except Exception as e:
                logger.warning(f"Strategy {i+1} failed: {e}")
                continue
        
        # If all strategies fail, use emergency fallback
        logger.error("All LLM strategies failed. Using emergency fallback.")
        return self._get_emergency_fallback_metrics(history, turn_number)
    
    def _get_qwen_json_strategy_1(self, conversation_text: str, turn_number: int) -> Optional[Dict]:
        """Qwen-specific strategy 1: Aggressive JSON-only with explicit instructions."""
        prompt = f"""JSON OUTPUT ONLY. NO EXPLANATIONS. NO THINKING. NO ADDITIONAL TEXT.

CONVERSATION:
{conversation_text}

OUTPUT ONLY THIS JSON (replace values with your analysis):
{{"customer_engagement":0.5,"sales_effectiveness":0.5,"conversation_length":3,"outcome":0.5,"progress":0.5,"conversation_style":"direct_professional","conversation_flow":"standard_linear","communication_channel":"email","primary_customer_needs":["efficiency","cost_reduction"],"engagement_trend":0.5,"objection_count":0.3,"value_proposition_mentions":0.4,"technical_depth":0.3,"urgency_level":0.2,"competitive_context":0.1,"pricing_sensitivity":0.4,"decision_authority_signals":0.5}}"""

        return self._execute_qwen_strategy(prompt, conversation_text)
    
    def _get_qwen_json_strategy_2(self, conversation_text: str, turn_number: int) -> Optional[Dict]:
        """Qwen-specific strategy 2: Direct instruction format."""
        prompt = f"""[INST] Analyze sales conversation. Return JSON only, no other text. [/INST]

{conversation_text}

{{"customer_engagement":0.5,"sales_effectiveness":0.5,"conversation_length":{len(conversation_text.split())//10},"outcome":0.5,"progress":0.5,"conversation_style":"direct_professional","conversation_flow":"standard_linear","communication_channel":"email","primary_customer_needs":["efficiency","cost_reduction"],"engagement_trend":0.5,"objection_count":0.3,"value_proposition_mentions":0.4,"technical_depth":0.3,"urgency_level":0.2,"competitive_context":0.1,"pricing_sensitivity":0.4,"decision_authority_signals":0.5}}"""

        return self._execute_qwen_strategy(prompt, conversation_text)
    
    def _get_qwen_json_strategy_3(self, conversation_text: str, turn_number: int) -> Optional[Dict]:
        """Qwen-specific strategy 3: System format without thinking."""
        try:
            messages = [
                {"role": "system", "content": "You are a JSON output system. Output valid JSON only. No thinking, no explanations, no additional text whatsoever."},
                {"role": "user", "content": f"Analyze: {conversation_text}\n\nJSON:"}
            ]
            
            chat_completion = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=200,
                temperature=0.0,  # Zero temperature for consistency
                top_p=0.1,        # Very focused sampling
                stop=["</s>", "<|im_end|>", "\n\n", "Analysis:", "Let me", "I'll", "To analyze", "Looking at"],
                repeat_penalty=1.0
            )
            raw_output = chat_completion['choices'][0]['message']['content'].strip()
            return self._extract_and_validate_json(raw_output, conversation_text)
            
        except Exception as e:
            logger.warning(f"Qwen strategy 3 execution failed: {e}")
            return None
    
    def _execute_qwen_strategy(self, prompt: str, conversation_text: str) -> Optional[Dict]:
        """Execute a Qwen-specific LLM strategy with optimized parameters."""
        try:
            llm_response = self.llm(
                prompt,
                max_tokens=200,
                temperature=0.0,      # Zero temperature for Qwen
                top_p=0.05,           # Very focused
                top_k=10,             # Limited vocabulary
                stop=["</s>", "<|im_end|>", "\n\n", "Okay", "Let me", "I'll", "To", "The", "Looking", "Analysis", "<think>", "```"],
                repeat_penalty=1.0,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            raw_output = llm_response['choices'][0]['text'].strip()
            
            # Remove common Qwen prefixes
            prefixes_to_remove = [
                "Okay,", "Let me", "I'll", "To analyze", "Looking at", "The conversation", 
                "Based on", "From the", "In this", "Here's", "This is", "Analysis:", 
                "<think>", "thinking:", "Let's"
            ]
            
            for prefix in prefixes_to_remove:
                if raw_output.lower().startswith(prefix.lower()):
                    # Find the JSON part
                    json_start = raw_output.find('{')
                    if json_start != -1:
                        raw_output = raw_output[json_start:]
                        break
            
            logger.debug(f"Qwen raw output (first 100 chars): {raw_output[:100]}...")
            
            return self._extract_and_validate_json(raw_output, conversation_text)
            
        except Exception as e:
            logger.warning(f"Qwen LLM execution failed: {e}")
            return None
    
    def _get_json_strategy_1(self, conversation_text: str, turn_number: int) -> Optional[Dict]:
        """Strategy 1: Direct JSON request with strong constraints."""
        prompt = f"""TASK: Analyze sales conversation and return ONLY a JSON object.

CONVERSATION:
{conversation_text}

RESPOND WITH ONLY THIS JSON STRUCTURE (no other text):
{{
  "customer_engagement": 0.5,
  "sales_effectiveness": 0.5,
  "conversation_length": 3,
  "outcome": 0.5,
  "progress": 0.5,
  "conversation_style": "direct_professional",
  "conversation_flow": "standard_linear",
  "communication_channel": "email",
  "primary_customer_needs": ["efficiency", "cost_reduction"],
  "engagement_trend": 0.5,
  "objection_count": 0.3,
  "value_proposition_mentions": 0.4,
  "technical_depth": 0.3,
  "urgency_level": 0.2,
  "competitive_context": 0.1,
  "pricing_sensitivity": 0.4,
  "decision_authority_signals": 0.5
}}

Replace the values with your analysis. Return ONLY the JSON object above."""

        return self._execute_llm_strategy(prompt, conversation_text)
    
    def _get_json_strategy_2(self, conversation_text: str, turn_number: int) -> Optional[Dict]:
        """Strategy 2: System/user message format with JSON enforcement."""
        system_prompt = "You are a JSON-only response system. You MUST respond with valid JSON and nothing else. No explanations, no markdown, no additional text."
        
        user_prompt = f"""Analyze this sales conversation and respond with ONLY a JSON object:

{conversation_text}

JSON format required:
{{"customer_engagement": 0.0-1.0, "sales_effectiveness": 0.0-1.0, "conversation_length": count, "outcome": 0.0-1.0, "progress": 0.0-1.0, "conversation_style": "string", "conversation_flow": "string", "communication_channel": "string", "primary_customer_needs": ["array"], "engagement_trend": 0.0-1.0, "objection_count": 0.0-1.0, "value_proposition_mentions": 0.0-1.0, "technical_depth": 0.0-1.0, "urgency_level": 0.0-1.0, "competitive_context": 0.0-1.0, "pricing_sensitivity": 0.0-1.0, "decision_authority_signals": 0.0-1.0}}"""

        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            chat_completion = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=300,
                temperature=0.1,
                stop=["```", "\n\n\n"]
            )
            raw_output = chat_completion['choices'][0]['message']['content'].strip()
            return self._extract_and_validate_json(raw_output, conversation_text)
            
        except Exception as e:
            logger.warning(f"Strategy 2 execution failed: {e}")
            return None
    
    def _get_json_strategy_3(self, conversation_text: str, turn_number: int) -> Optional[Dict]:
        """Strategy 3: Simple direct prompt with minimal context."""
        prompt = f"""Sales conversation analysis. Return valid JSON only:

{conversation_text}

{{"customer_engagement":0.5,"sales_effectiveness":0.5,"conversation_length":3,"outcome":0.5,"progress":0.5,"conversation_style":"direct_professional","conversation_flow":"standard_linear","communication_channel":"email","primary_customer_needs":["efficiency","cost_reduction"],"engagement_trend":0.5,"objection_count":0.3,"value_proposition_mentions":0.4,"technical_depth":0.3,"urgency_level":0.2,"competitive_context":0.1,"pricing_sensitivity":0.4,"decision_authority_signals":0.5}}"""

        return self._execute_llm_strategy(prompt, conversation_text)
    
    def _execute_llm_strategy(self, prompt: str, conversation_text: str) -> Optional[Dict]:
        """Execute a single LLM strategy."""
        try:
            llm_response = self.llm(
                prompt,
                max_tokens=300,
                temperature=0.05,  # Very low temperature for consistency
                stop=["```", "\n\n", "Analysis:", "Explanation:"],
                repeat_penalty=1.1
            )
            raw_output = llm_response['choices'][0]['text'].strip()
            logger.debug(f"Raw LLM output: {raw_output[:200]}...")
            
            return self._extract_and_validate_json(raw_output, conversation_text)
            
        except Exception as e:
            logger.warning(f"LLM execution failed: {e}")
            return None
    
    def _extract_and_validate_json(self, raw_output: str, conversation_text: str) -> Optional[Dict]:
        """Extract and validate JSON from LLM output with multiple extraction methods."""
        # For Qwen models, try more aggressive cleaning first
        if self.is_qwen_model:
            raw_output = self._clean_qwen_output(raw_output)
        
        # Method 1: Look for JSON object
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw_output, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                parsed_json = json.loads(json_str)
                validated = self._validate_and_normalize_all_metrics(parsed_json, [], 0)
                logger.debug("Successfully extracted JSON using method 1")
                return validated
            except json.JSONDecodeError:
                pass
        
        # Method 2: Try to fix common JSON issues
        cleaned_output = raw_output
        # Remove markdown
        cleaned_output = re.sub(r'```json\s*', '', cleaned_output)
        cleaned_output = re.sub(r'```\s*', '', cleaned_output)
        # Remove explanatory text before/after JSON
        lines = cleaned_output.split('\n')
        json_lines = []
        in_json = False
        
        for line in lines:
            if '{' in line and not in_json:
                in_json = True
            if in_json:
                json_lines.append(line)
            if '}' in line and in_json:
                break
        
        if json_lines:
            json_str = '\n'.join(json_lines)
            try:
                parsed_json = json.loads(json_str)
                validated = self._validate_and_normalize_all_metrics(parsed_json, [], 0)
                logger.debug("Successfully extracted JSON using method 2")
                return validated
            except json.JSONDecodeError:
                pass
        
        # Method 3: Create from patterns
        try:
            # Extract individual values using regex
            patterns = {
                'customer_engagement': r'["\']?customer_engagement["\']?\s*:\s*([0-9.]+)',
                'sales_effectiveness': r'["\']?sales_effectiveness["\']?\s*:\s*([0-9.]+)',
                'outcome': r'["\']?outcome["\']?\s*:\s*([0-9.]+)',
            }
            
            extracted_values = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, raw_output)
                if match:
                    extracted_values[key] = float(match.group(1))
            
            if len(extracted_values) >= 2:  # At least 2 values found
                # Create a basic JSON structure
                json_obj = {
                    'customer_engagement': extracted_values.get('customer_engagement', 0.5),
                    'sales_effectiveness': extracted_values.get('sales_effectiveness', 0.5),
                    'conversation_length': len(conversation_text.split('\n')),
                    'outcome': extracted_values.get('outcome', 0.5),
                    'progress': 0.5,
                    'conversation_style': 'direct_professional',
                    'conversation_flow': 'standard_linear',
                    'communication_channel': 'email',
                    'primary_customer_needs': ['efficiency', 'cost_reduction'],
                    'engagement_trend': 0.5,
                    'objection_count': 0.3,
                    'value_proposition_mentions': 0.4,
                    'technical_depth': 0.3,
                    'urgency_level': 0.2,
                    'competitive_context': 0.1,
                    'pricing_sensitivity': 0.4,
                    'decision_authority_signals': 0.5
                }
                
                validated = self._validate_and_normalize_all_metrics(json_obj, [], 0)
                logger.debug("Successfully extracted JSON using method 3 (pattern matching)")
                return validated
        
        except Exception as e:
            logger.warning(f"Pattern extraction failed: {e}")
        
        logger.warning(f"All JSON extraction methods failed for output: {raw_output[:100]}...")
        return None
    
    def _clean_qwen_output(self, raw_output: str) -> str:
        """Clean Qwen-specific output patterns."""
        # Remove common Qwen thinking patterns
        qwen_patterns = [
            r'<think>.*?</think>',
            r'Do not add any other text\.\s*',
            r'Okay,?\s*let\'?s tackle this\.?\s*',
            r'The user (provided|wants).*?\.',
            r'I need to analyze.*?\.',
            r'Let me analyze.*?\.',
            r'Looking at.*?\.',
            r'Based on.*?\.',
            r'From the conversation.*?\.',
        ]
        
        cleaned = raw_output
        for pattern in qwen_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.DOTALL)
        
        # Find the JSON part more aggressively
        json_start = cleaned.find('{')
        if json_start > 50:  # If JSON starts way after beginning, extract it
            cleaned = cleaned[json_start:]
        
        return cleaned.strip()

    def _validate_and_normalize_all_metrics(self, parsed_json: Dict, history: List[Dict[str, str]], turn_number: int) -> Dict:
        """Validate and normalize ALL LLM-provided metrics (core + derived) with robust error handling."""
        validated = {}
        
        try:
            # CORE METRICS (required for PPO model)
            core_numeric_fields = [
                'customer_engagement', 'sales_effectiveness', 'outcome', 'progress'
            ]
            
            for field in core_numeric_fields:
                value = parsed_json.get(field, 0.5)
                try:
                    if isinstance(value, (int, float)):
                        validated[field] = float(np.clip(value, 0.0, 1.0))
                    elif isinstance(value, str):
                        # Try to convert string to float
                        validated[field] = float(np.clip(float(value), 0.0, 1.0))
                    else:
                        logger.warning(f"Invalid {field} value type: {type(value)}, using 0.5")
                        validated[field] = 0.5
                except (ValueError, TypeError):
                    logger.warning(f"Could not convert {field} value: {value}, using 0.5")
                    validated[field] = 0.5
            
            # Conversation length (special core metric - should be actual count)
            conv_length = parsed_json.get('conversation_length', len(history))
            try:
                if isinstance(conv_length, (int, float)) and conv_length >= 0:
                    validated['conversation_length'] = float(conv_length)
                else:
                    validated['conversation_length'] = float(len(history))
            except (ValueError, TypeError):
                validated['conversation_length'] = float(len(history))
            
            # DERIVED BEHAVIORAL METRICS (all numeric 0.0-1.0)
            derived_numeric_fields = [
                'engagement_trend', 'objection_count', 'value_proposition_mentions', 
                'technical_depth', 'urgency_level', 'competitive_context', 
                'pricing_sensitivity', 'decision_authority_signals'
            ]
            
            for field in derived_numeric_fields:
                value = parsed_json.get(field, 0.5)
                try:
                    if isinstance(value, (int, float)):
                        validated[field] = float(np.clip(value, 0.0, 1.0))
                    elif isinstance(value, str):
                        validated[field] = float(np.clip(float(value), 0.0, 1.0))
                    else:
                        logger.warning(f"Invalid {field} value type: {type(value)}, using 0.5")
                        validated[field] = 0.5
                except (ValueError, TypeError):
                    logger.warning(f"Could not convert {field} value: {value}, using 0.5")
                    validated[field] = 0.5
            
            # STRING CATEGORICAL FIELDS with validation
            style_options = [
                "casual_friendly", "direct_professional", "technical_detailed", "consultative_advisory",
                "empathetic_supportive", "skeptical_challenging", "urgent_time_pressed", "confused_overwhelmed",
                "knowledgeable_assertive", "storytelling_narrative"
            ]
            style_value = parsed_json.get('conversation_style', 'direct_professional')
            validated['conversation_style'] = style_value if style_value in style_options else 'direct_professional'
            if style_value not in style_options:
                logger.warning(f"Invalid conversation_style: {style_value}, using direct_professional")
            
            flow_options = [
                "standard_linear", "multiple_objection_loops", "subject_switching", "interrupted_followup",
                "technical_deep_dive", "competitive_comparison", "gradual_discovery", "immediate_interest",
                "initial_rejection", "stakeholder_expansion", "pricing_negotiation", "implementation_concerns",
                "value_justification", "relationship_building", "multi_session", "demo_walkthrough"
            ]
            flow_value = parsed_json.get('conversation_flow', 'standard_linear')
            validated['conversation_flow'] = flow_value if flow_value in flow_options else 'standard_linear'
            if flow_value not in flow_options:
                logger.warning(f"Invalid conversation_flow: {flow_value}, using standard_linear")
            
            channel_options = ["email", "live_chat", "phone_call", "video_call", "in_person", "sms", "social_media"]
            channel_value = parsed_json.get('communication_channel', 'email')
            validated['communication_channel'] = channel_value if channel_value in channel_options else 'email'
            if channel_value not in channel_options:
                logger.warning(f"Invalid communication_channel: {channel_value}, using email")
            
            # ARRAY FIELD for customer needs with validation
            need_options = [
                "efficiency", "cost_reduction", "growth", "compliance", "integration",
                "usability", "reliability", "security", "support", "analytics"
            ]
            needs = parsed_json.get('primary_customer_needs', ['efficiency', 'cost_reduction'])
            try:
                if isinstance(needs, list):
                    validated_needs = []
                    for need in needs:
                        if isinstance(need, str) and need in need_options:
                            validated_needs.append(need)
                    validated['primary_customer_needs'] = validated_needs[:3] if validated_needs else ['efficiency', 'cost_reduction']
                else:
                    logger.warning(f"Invalid primary_customer_needs type: {type(needs)}, using default")
                    validated['primary_customer_needs'] = ['efficiency', 'cost_reduction']
            except Exception:
                logger.warning(f"Error processing primary_customer_needs: {needs}, using default")
                validated['primary_customer_needs'] = ['efficiency', 'cost_reduction']
            
            if not validated['primary_customer_needs']:
                validated['primary_customer_needs'] = ['efficiency', 'cost_reduction']
            
            logger.debug(f"Successfully validated metrics with {len(validated)} fields")
            return validated
            
        except Exception as e:
            logger.error(f"Error in validation: {e}", exc_info=True)
            logger.warning("Validation failed, using emergency fallback")
            return self._get_emergency_fallback_metrics(history, turn_number)

    def _get_emergency_fallback_metrics(self, history: List[Dict[str, str]], turn_number: int) -> Dict:
        """Intelligent emergency fallback when LLM completely fails - enhanced analysis."""
        logger.error("Using enhanced emergency fallback metrics - this indicates LLM instruction-following failure")
        
        # Enhanced analysis based on conversation content
        conversation_length = len(history)
        customer_messages = [msg['message'].lower() for msg in history if msg['speaker'] == 'customer']
        sales_messages = [msg['message'].lower() for msg in history if msg['speaker'] == 'sales_rep']
        
        customer_text = " ".join(customer_messages)
        sales_text = " ".join(sales_messages)
        
        # Analyze customer engagement signals
        positive_signals = ['interested', 'yes', 'sounds good', 'tell me more', 'what about', 'how does', 'can you', 'would like', 'want to', 'need', 'looking for']
        negative_signals = ['not interested', 'no', 'expensive', 'too much', 'costly', 'bye', 'goodbye', 'not for us', 'maybe later', 'not now']
        neutral_signals = ['ok', 'maybe', 'i see', 'understand', 'hmm', 'let me think']
        
        positive_count = sum(1 for signal in positive_signals if signal in customer_text)
        negative_count = sum(1 for signal in negative_signals if signal in customer_text) 
        neutral_count = sum(1 for signal in neutral_signals if signal in customer_text)
        
        # Calculate engagement based on signals and message length
        if positive_count > negative_count:
            base_engagement = 0.6 + min(0.3, positive_count * 0.1)
        elif negative_count > positive_count:
            base_engagement = 0.4 - min(0.3, negative_count * 0.1)
        else:
            base_engagement = 0.5
            
        # Adjust for conversation length and detail
        avg_customer_msg_length = np.mean([len(msg) for msg in customer_messages]) if customer_messages else 20
        if avg_customer_msg_length > 50:
            base_engagement += 0.1  # Longer messages suggest engagement
        elif avg_customer_msg_length < 15:
            base_engagement -= 0.1  # Very short messages suggest disengagement
            
        # Analyze sales effectiveness
        sales_value_words = ['benefit', 'advantage', 'solution', 'help', 'save', 'improve', 'increase', 'reduce', 'roi', 'value']
        sales_question_words = ['what', 'how', 'when', 'where', 'why', 'tell me', 'can you']
        
        value_mentions = sum(1 for word in sales_value_words if word in sales_text)
        question_count = sum(1 for word in sales_question_words if word in sales_text)
        
        base_effectiveness = 0.5
        if value_mentions > 0:
            base_effectiveness += min(0.2, value_mentions * 0.05)
        if question_count > 0:
            base_effectiveness += min(0.15, question_count * 0.03)
            
        # Assess sales rep responsiveness
        if len(sales_messages) > 0:
            avg_sales_msg_length = np.mean([len(msg) for msg in sales_messages])
            if avg_sales_msg_length < 10:  # Very short responses
                base_effectiveness -= 0.2
        
        # Determine outcome probability
        if 'bye' in customer_text or 'goodbye' in customer_text or 'not interested' in customer_text:
            outcome = 0.1
        elif positive_count > negative_count * 2:
            outcome = 0.7
        elif negative_count > positive_count:
            outcome = 0.2
        else:
            outcome = 0.4
            
        # Determine conversation style
        if any(word in customer_text for word in ['technical', 'integration', 'api', 'security']):
            conv_style = 'technical_detailed'
        elif any(word in customer_text for word in ['budget', 'cost', 'price', 'expensive']):
            conv_style = 'skeptical_challenging'
        elif len(customer_text) > 200:
            conv_style = 'consultative_advisory'
        else:
            conv_style = 'direct_professional'
            
        # Determine conversation flow
        if negative_count > 1:
            conv_flow = 'multiple_objection_loops'
        elif 'price' in customer_text or 'cost' in customer_text:
            conv_flow = 'pricing_negotiation'
        elif conversation_length < 4:
            conv_flow = 'immediate_interest' if positive_count > 0 else 'initial_rejection'
        else:
            conv_flow = 'standard_linear'
            
        # Pricing sensitivity analysis
        pricing_sensitivity = 0.3
        if any(word in customer_text for word in ['expensive', 'costly', 'budget', 'cheap', 'affordable']):
            pricing_sensitivity = 0.8
        elif any(word in customer_text for word in ['price', 'cost', 'pricing']):
            pricing_sensitivity = 0.6
            
        return {
            # Core metrics with enhanced analysis
            'customer_engagement': float(np.clip(base_engagement, 0.0, 1.0)),
            'sales_effectiveness': float(np.clip(base_effectiveness, 0.0, 1.0)),
            'conversation_length': float(conversation_length),
            'outcome': float(np.clip(outcome, 0.0, 1.0)),
            'progress': min(1.0, turn_number / self.MAX_TURNS_REFERENCE),
            
            # Enhanced categorical metrics
            'conversation_style': conv_style,
            'conversation_flow': conv_flow,
            'communication_channel': 'email',  # Default assumption
            'primary_customer_needs': self._infer_customer_needs(customer_text),
            
            # Enhanced behavioral metrics
            'engagement_trend': 0.3 if negative_count > positive_count else 0.7 if positive_count > negative_count else 0.5,
            'objection_count': float(np.clip(negative_count / max(1, conversation_length), 0.0, 1.0)),
            'value_proposition_mentions': float(np.clip(value_mentions / max(1, len(sales_messages)), 0.0, 1.0)),
            'technical_depth': 0.7 if any(word in customer_text for word in ['technical', 'integration', 'api']) else 0.3,
            'urgency_level': 0.7 if any(word in customer_text for word in ['urgent', 'asap', 'quickly', 'soon']) else 0.2,
            'competitive_context': 0.6 if any(word in customer_text for word in ['competitor', 'alternative', 'vs', 'compare']) else 0.1,
            'pricing_sensitivity': pricing_sensitivity,
            'decision_authority_signals': 0.7 if any(phrase in customer_text for phrase in ['i decide', 'my budget', 'i approve']) else 0.3
        }
    
    def _infer_customer_needs(self, customer_text: str) -> List[str]:
        """Infer customer needs from their messages."""
        need_keywords = {
            'efficiency': ['efficient', 'streamline', 'automate', 'faster', 'time'],
            'cost_reduction': ['save', 'cost', 'budget', 'expensive', 'affordable', 'roi'],
            'growth': ['grow', 'scale', 'expand', 'increase', 'more'],
            'integration': ['integrate', 'connect', 'work with', 'compatible'],
            'usability': ['easy', 'simple', 'user-friendly', 'intuitive'],
            'security': ['secure', 'security', 'safe', 'protect'],
            'support': ['help', 'support', 'training', 'assistance'],
            'analytics': ['report', 'analytics', 'data', 'insights', 'dashboard']
        }
        
        detected_needs = []
        for need, keywords in need_keywords.items():
            if any(keyword in customer_text for keyword in keywords):
                detected_needs.append(need)
        
        # Return top 3 or default
        return detected_needs[:3] if detected_needs else ['efficiency', 'cost_reduction']

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
        """Analyze conversation metrics using LLM for ALL metrics with robust error handling."""
        
        try:
            # Get ALL metrics from LLM (core + derived) with multiple strategies
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
            
            # Verify all required keys are present
            required_keys = [
                'customer_engagement', 'sales_effectiveness', 'conversation_length', 
                'outcome', 'progress', 'conversation_style', 'conversation_flow',
                'communication_channel', 'primary_customer_needs', 'engagement_trend',
                'objection_count', 'value_proposition_mentions', 'technical_depth',
                'urgency_level', 'competitive_context', 'pricing_sensitivity',
                'decision_authority_signals', 'probability_trajectory'
            ]
            
            for key in required_keys:
                if key not in all_metrics:
                    logger.warning(f"Missing key {key} in metrics, adding default")
                    all_metrics[key] = 0.5 if key not in ['conversation_style', 'conversation_flow', 'communication_channel', 'primary_customer_needs', 'probability_trajectory'] else self._get_default_value(key)
            
            return all_metrics
            
        except Exception as e:
            logger.error(f"Critical error in analyze_metrics: {e}", exc_info=True)
            logger.error("Falling back to emergency metrics due to critical error")
            
            # Last resort fallback
            emergency_metrics = self._get_emergency_fallback_metrics(history, turn_number)
            emergency_metrics['probability_trajectory'] = {i: 0.4 for i in range(len(history))}
            return emergency_metrics
    
    def _get_default_value(self, key: str):
        """Get default values for non-numeric keys."""
        defaults = {
            'conversation_style': 'direct_professional',
            'conversation_flow': 'standard_linear', 
            'communication_channel': 'email',
            'primary_customer_needs': ['efficiency', 'cost_reduction'],
            'probability_trajectory': {}
        }
        return defaults.get(key, 0.5)

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