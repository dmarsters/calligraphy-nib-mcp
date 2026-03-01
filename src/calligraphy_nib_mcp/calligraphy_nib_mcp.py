"""
Calligraphy Nib Visual Vocabulary MCP Server

Three-layer olog architecture for deterministic nib→visual parameter mapping.
Zero-cost taxonomy operations + targeted synthesis interface.

Layer 1: Nib taxonomy (tine structure, material, geometry)
Layer 2: Deterministic visual parameter mapping
Layer 3: Interface for LLM synthesis of image prompts
"""

from fastmcp import FastMCP
from typing import Dict, List, Any, Optional, Tuple
import json
import math
import numpy as np

mcp = FastMCP("calligraphy-nib")

# ============================================================================
# LAYER 1: NIB TAXONOMY (Pure Lookup - 0 tokens)
# ============================================================================

NIB_TYPES = {
    "pointed_flexible": {
        "name": "Pointed Flexible Nib",
        "tine_structure": "split",
        "material": "steel",
        "tip_geometry": "pointed",
        "flex_characteristics": "full-flex",
        "optimal_use": ["copperplate", "spencerian", "ornamental"],
        "stroke_width_ratio": "10:1",
        "description": "Classic fine-pointed nib with high flex for dramatic thick/thin contrast"
    },
    "pointed_rigid": {
        "name": "Pointed Rigid Nib",
        "tine_structure": "split",
        "material": "steel",
        "tip_geometry": "pointed",
        "flex_characteristics": "rigid",
        "optimal_use": ["modern_pointed", "business_script"],
        "stroke_width_ratio": "3:1",
        "description": "Fine point with minimal flex for controlled, consistent strokes"
    },
    "broad_edge_square": {
        "name": "Square-Cut Broad Edge",
        "tine_structure": "single",
        "material": "steel",
        "tip_geometry": "square-cut",
        "flex_characteristics": "rigid",
        "optimal_use": ["italic", "gothic", "uncial"],
        "stroke_width_ratio": "5:1",
        "description": "Flat chisel edge creating strong vertical emphasis"
    },
    "broad_edge_stub": {
        "name": "Stub Nib",
        "tine_structure": "single",
        "material": "steel",
        "tip_geometry": "rounded",
        "flex_characteristics": "rigid",
        "optimal_use": ["italic", "modern_calligraphy"],
        "stroke_width_ratio": "3:1",
        "description": "Rounded broad edge for softer stroke contrast"
    },
    "oblique_left": {
        "name": "Left-Oblique Broad Edge",
        "tine_structure": "single",
        "material": "steel",
        "tip_geometry": "oblique",
        "flex_characteristics": "rigid",
        "optimal_use": ["italic", "humanist"],
        "stroke_width_ratio": "5:1",
        "description": "Angled edge emphasizing horizontal strokes"
    },
    "oblique_right": {
        "name": "Right-Oblique Broad Edge",
        "tine_structure": "single",
        "material": "steel",
        "tip_geometry": "oblique",
        "flex_characteristics": "rigid",
        "optimal_use": ["specialized_styles"],
        "stroke_width_ratio": "5:1",
        "description": "Reverse-angled edge for unconventional stress patterns"
    },
    "copperplate_gold": {
        "name": "Gold Copperplate Nib",
        "tine_structure": "split",
        "material": "gold",
        "tip_geometry": "pointed",
        "flex_characteristics": "semi-flex",
        "optimal_use": ["copperplate", "spencerian"],
        "stroke_width_ratio": "7:1",
        "description": "Precious metal nib with warm flex response"
    },
    "monoline_round": {
        "name": "Monoline Round Point",
        "tine_structure": "single",
        "material": "steel",
        "tip_geometry": "round-point",
        "flex_characteristics": "rigid",
        "optimal_use": ["technical", "modern"],
        "stroke_width_ratio": "1:1",
        "description": "Consistent width in all directions, no stroke modulation"
    },
    "glass_dip": {
        "name": "Glass Dip Nib",
        "tine_structure": "single",
        "material": "glass",
        "tip_geometry": "needle-point",
        "flex_characteristics": "rigid",
        "optimal_use": ["ultra-fine", "detailed"],
        "stroke_width_ratio": "1:1",
        "description": "Ultra-fine point for microscopic detail work"
    },
    "scroll_nib": {
        "name": "Scroll/Ornamental Nib",
        "tine_structure": "split",
        "material": "brass",
        "tip_geometry": "pointed",
        "flex_characteristics": "full-flex",
        "optimal_use": ["flourishing", "ornamental"],
        "stroke_width_ratio": "15:1",
        "description": "Extreme flex for dramatic ornamental swells"
    }
}

# ============================================================================
# VISUAL VOCABULARY MAPPINGS (Deterministic - 0 tokens)
# ============================================================================

VISUAL_PARAMETERS = {
    # Line Quality Characteristics
    "line_quality": {
        "pointed_flexible": {
            "stroke_dynamics": "dramatic_swell",
            "edge_characteristics": "crisp_boundaries",
            "texture_signature": "smooth_glide",
            "width_variation": "extreme_contrast",
            "keywords": ["hairline entrance", "pressure swell", "shade release", "elastic taper"]
        },
        "pointed_rigid": {
            "stroke_dynamics": "controlled_swell",
            "edge_characteristics": "crisp_boundaries",
            "texture_signature": "smooth_glide",
            "width_variation": "moderate_contrast",
            "keywords": ["consistent baseline", "predictable width", "controlled taper", "clean edges"]
        },
        "broad_edge_square": {
            "stroke_dynamics": "geometric",
            "edge_characteristics": "sharp_terminals",
            "texture_signature": "paper_tooth_interaction",
            "width_variation": "angular_dependent",
            "keywords": ["vertical shades", "horizontal hairlines", "square terminals", "chisel edge"]
        },
        "broad_edge_stub": {
            "stroke_dynamics": "geometric",
            "edge_characteristics": "soft_terminals",
            "texture_signature": "smooth_glide",
            "width_variation": "angular_dependent",
            "keywords": ["vertical emphasis", "rounded terminals", "soft contrast", "flowing strokes"]
        },
        "oblique_left": {
            "stroke_dynamics": "geometric",
            "edge_characteristics": "angled_terminals",
            "texture_signature": "directional_resistance",
            "width_variation": "horizontal_emphasis",
            "keywords": ["horizontal shades", "vertical hairlines", "oblique stress", "angular terminals"]
        },
        "oblique_right": {
            "stroke_dynamics": "geometric",
            "edge_characteristics": "angled_terminals",
            "texture_signature": "directional_resistance",
            "width_variation": "reverse_stress",
            "keywords": ["unconventional stress", "reverse emphasis", "angular terminals"]
        },
        "copperplate_gold": {
            "stroke_dynamics": "warm_swell",
            "edge_characteristics": "soft_boundaries",
            "texture_signature": "butter_smooth",
            "width_variation": "high_contrast",
            "keywords": ["warm flex", "generous swell", "soft edges", "flowing taper"]
        },
        "monoline_round": {
            "stroke_dynamics": "uniform",
            "edge_characteristics": "consistent_width",
            "texture_signature": "smooth_glide",
            "width_variation": "no_variation",
            "keywords": ["constant width", "omni-directional", "even pressure", "consistent flow"]
        },
        "glass_dip": {
            "stroke_dynamics": "ultra_fine",
            "edge_characteristics": "razor_sharp",
            "texture_signature": "micro_control",
            "width_variation": "minimal",
            "keywords": ["needle point", "microscopic detail", "ultra crisp", "precision line"]
        },
        "scroll_nib": {
            "stroke_dynamics": "extreme_swell",
            "edge_characteristics": "ornamental_flair",
            "texture_signature": "variable_flow",
            "width_variation": "maximum_contrast",
            "keywords": ["dramatic flourish", "extreme swell", "ornamental shade", "spectacular taper"]
        }
    },
    
    # Ink Flow Characteristics
    "ink_behavior": {
        "pointed_flexible": {
            "deposit_pattern": "controlled_metering",
            "flow_rate": "moderate",
            "pressure_response": "exponential",
            "keywords": ["clean feed", "pressure-responsive", "controlled release", "no pooling"]
        },
        "broad_edge_square": {
            "deposit_pattern": "generous_flow",
            "flow_rate": "heavy",
            "pressure_response": "linear",
            "keywords": ["saturated line", "edge definition", "consistent deposit", "rich black"]
        },
        "copperplate_gold": {
            "deposit_pattern": "wet_generous",
            "flow_rate": "abundant",
            "pressure_response": "threshold_snap",
            "keywords": ["liquid flow", "smooth deposit", "snap flex", "warm saturation"]
        },
        "glass_dip": {
            "deposit_pattern": "minimal_metering",
            "flow_rate": "light",
            "pressure_response": "linear",
            "keywords": ["fine line", "delicate deposit", "crisp definition", "no bleed"]
        }
    },
    
    # Directional Properties
    "directional_emphasis": {
        "broad_edge_square": {
            "primary_axis": "vertical",
            "optimal_angle": "45°",
            "stress_pattern": "vertical_dominant",
            "keywords": ["vertical shades", "horizontal hairlines", "45-degree hold"]
        },
        "oblique_left": {
            "primary_axis": "horizontal",
            "optimal_angle": "45°",
            "stress_pattern": "horizontal_dominant",
            "keywords": ["horizontal shades", "vertical hairlines", "oblique stress"]
        },
        "pointed_flexible": {
            "primary_axis": "omnidirectional",
            "optimal_angle": "varies",
            "stress_pattern": "pressure_dependent",
            "keywords": ["rotation freedom", "angle modulation", "pressure stress"]
        },
        "monoline_round": {
            "primary_axis": "omnidirectional",
            "optimal_angle": "any",
            "stress_pattern": "isotropic",
            "keywords": ["no directional bias", "rotation independent", "uniform stress"]
        }
    }
}

# ============================================================================
# PHASE 2.6: NORMALIZED 5D PARAMETER SPACE
# ============================================================================
# Maps every nib type to a normalized [0.0, 1.0] coordinate in 5 dimensions.
# Enables trajectory computation, rhythmic composition, and multi-domain
# composition via aesthetic-dynamics-core.

CALLIGRAPHY_PARAMETER_NAMES = [
    "stroke_contrast",    # 0.0 = monoline uniform → 1.0 = extreme thick/thin
    "edge_sharpness",     # 0.0 = soft/rounded terminals → 1.0 = razor/crisp
    "flex_response",      # 0.0 = rigid (no pressure variation) → 1.0 = full flex
    "directional_bias",   # 0.0 = omnidirectional → 1.0 = strongly angle-dependent
    "ink_richness"        # 0.0 = minimal/dry → 1.0 = abundant/saturated
]

CALLIGRAPHY_COORDS = {
    "pointed_flexible": {
        "stroke_contrast": 0.85,
        "edge_sharpness": 0.80,
        "flex_response": 0.90,
        "directional_bias": 0.15,
        "ink_richness": 0.55
    },
    "pointed_rigid": {
        "stroke_contrast": 0.35,
        "edge_sharpness": 0.75,
        "flex_response": 0.15,
        "directional_bias": 0.10,
        "ink_richness": 0.50
    },
    "broad_edge_square": {
        "stroke_contrast": 0.65,
        "edge_sharpness": 0.90,
        "flex_response": 0.10,
        "directional_bias": 0.90,
        "ink_richness": 0.70
    },
    "broad_edge_stub": {
        "stroke_contrast": 0.40,
        "edge_sharpness": 0.15,
        "flex_response": 0.10,
        "directional_bias": 0.75,
        "ink_richness": 0.65
    },
    "oblique_left": {
        "stroke_contrast": 0.65,
        "edge_sharpness": 0.70,
        "flex_response": 0.10,
        "directional_bias": 0.95,
        "ink_richness": 0.65
    },
    "oblique_right": {
        "stroke_contrast": 0.65,
        "edge_sharpness": 0.70,
        "flex_response": 0.10,
        "directional_bias": 0.95,
        "ink_richness": 0.60
    },
    "copperplate_gold": {
        "stroke_contrast": 0.75,
        "edge_sharpness": 0.45,
        "flex_response": 0.65,
        "directional_bias": 0.20,
        "ink_richness": 0.90
    },
    "monoline_round": {
        "stroke_contrast": 0.00,
        "edge_sharpness": 0.30,
        "flex_response": 0.00,
        "directional_bias": 0.00,
        "ink_richness": 0.50
    },
    "glass_dip": {
        "stroke_contrast": 0.05,
        "edge_sharpness": 1.00,
        "flex_response": 0.00,
        "directional_bias": 0.05,
        "ink_richness": 0.10
    },
    "scroll_nib": {
        "stroke_contrast": 1.00,
        "edge_sharpness": 0.60,
        "flex_response": 1.00,
        "directional_bias": 0.25,
        "ink_richness": 0.75
    }
}

# ============================================================================
# PHASE 2.6: RHYTHMIC PRESETS
# ============================================================================
# Five presets oscillating between canonical nib states.
# Period selection strategy:
#   [11, 14, 18, 22, 28]
#   - 11: Fills gap near 10, prime period for beat complexity
#   - 14: Fills gap between 12 and 15 (2×7)
#   - 18: Shared with nuclear/catastrophe/diatom for cross-domain resonance
#   - 22: Shared with catastrophe/heraldic for cross-domain resonance
#   - 28: Creates resonance with the Period 28 composite beat mechanism

CALLIGRAPHY_RHYTHMIC_PRESETS = {
    "pressure_swell_cycle": {
        "state_a": "pointed_rigid",
        "state_b": "pointed_flexible",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 22,
        "description": "Flex response oscillation: controlled precision ↔ dramatic pressure swell"
    },
    "edge_transition": {
        "state_a": "broad_edge_square",
        "state_b": "broad_edge_stub",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 14,
        "description": "Terminal quality shift: sharp geometric ↔ soft rounded edges"
    },
    "material_warmth": {
        "state_a": "pointed_rigid",
        "state_b": "copperplate_gold",
        "pattern": "triangular",
        "num_cycles": 3,
        "steps_per_cycle": 18,
        "description": "Material character progression: steel precision ↔ gold warmth"
    },
    "contrast_spectrum": {
        "state_a": "monoline_round",
        "state_b": "scroll_nib",
        "pattern": "sinusoidal",
        "num_cycles": 2,
        "steps_per_cycle": 28,
        "description": "Full contrast range: uniform monoline ↔ extreme ornamental swell"
    },
    "precision_flourish": {
        "state_a": "glass_dip",
        "state_b": "scroll_nib",
        "pattern": "square",
        "num_cycles": 5,
        "steps_per_cycle": 11,
        "description": "Rapid toggle: ultra-fine precision ↔ dramatic ornamental flourish"
    }
}

# ============================================================================
# PHASE 2.7: VISUAL TYPE VOCABULARY FOR ATTRACTOR VISUALIZATION
# ============================================================================
# Maps regions of the 5D calligraphy parameter space to image-generation-ready
# visual vocabulary. Used by generate_attractor_visualization_prompt().

CALLIGRAPHY_VISUAL_TYPES = {
    "copperplate_elegance": {
        "coords": {
            "stroke_contrast": 0.75,
            "edge_sharpness": 0.45,
            "flex_response": 0.65,
            "directional_bias": 0.20,
            "ink_richness": 0.90
        },
        "keywords": [
            "flowing copperplate script",
            "warm pressure swells",
            "elastic shade strokes",
            "generous ink saturation",
            "golden pen warmth",
            "organic thick-thin transitions"
        ],
        "optical_properties": {
            "surface_quality": "wet_lustre",
            "light_interaction": "warm_specular",
            "depth_cue": "ink_pooling_at_swells"
        },
        "color_associations": ["warm black", "sepia", "walnut ink", "iron gall"]
    },
    "gothic_architecture": {
        "coords": {
            "stroke_contrast": 0.65,
            "edge_sharpness": 0.90,
            "flex_response": 0.10,
            "directional_bias": 0.90,
            "ink_richness": 0.70
        },
        "keywords": [
            "architectural blackletter strokes",
            "sharp diamond terminals",
            "vertical shade columns",
            "geometric stroke pattern",
            "dense ink coverage",
            "angular calligraphic forms"
        ],
        "optical_properties": {
            "surface_quality": "matte_dense",
            "light_interaction": "high_contrast_absorption",
            "depth_cue": "carved_letterform_relief"
        },
        "color_associations": ["lamp black", "carbon black", "dark as wrought iron"]
    },
    "modern_minimal": {
        "coords": {
            "stroke_contrast": 0.05,
            "edge_sharpness": 0.30,
            "flex_response": 0.00,
            "directional_bias": 0.00,
            "ink_richness": 0.50
        },
        "keywords": [
            "monoline lettering",
            "consistent stroke weight",
            "clean geometric forms",
            "uniform line quality",
            "minimalist letterforms",
            "technical precision drawing"
        ],
        "optical_properties": {
            "surface_quality": "even_matte",
            "light_interaction": "neutral_absorption",
            "depth_cue": "flat_graphic"
        },
        "color_associations": ["neutral grey", "steel blue-black", "balanced density"]
    },
    "ornamental_flourish": {
        "coords": {
            "stroke_contrast": 1.00,
            "edge_sharpness": 0.60,
            "flex_response": 1.00,
            "directional_bias": 0.25,
            "ink_richness": 0.75
        },
        "keywords": [
            "dramatic ornamental swells",
            "extreme thick-thin contrast",
            "flourishing spirals and loops",
            "spectacular ink shading gradients",
            "expressive calligraphic gesture",
            "baroque pen stroke virtuosity"
        ],
        "optical_properties": {
            "surface_quality": "variable_gloss",
            "light_interaction": "dynamic_reflection",
            "depth_cue": "ink_density_gradient"
        },
        "color_associations": ["deep black crescendos", "translucent hairlines", "rich swell pools"]
    },
    "precision_drafting": {
        "coords": {
            "stroke_contrast": 0.05,
            "edge_sharpness": 1.00,
            "flex_response": 0.00,
            "directional_bias": 0.05,
            "ink_richness": 0.10
        },
        "keywords": [
            "ultra-fine drafting lines",
            "needle-point precision marks",
            "microscopic ink detail",
            "delicate hairline traces",
            "technical illustration quality",
            "crisp definition edges"
        ],
        "optical_properties": {
            "surface_quality": "dry_precise",
            "light_interaction": "minimal_reflection",
            "depth_cue": "surface_scratch_quality"
        },
        "color_associations": ["pale grey", "light graphite trace", "whisper-thin ink"]
    }
}

@mcp.tool()
def list_nib_types() -> str:
    """
    List all available calligraphy nib types with descriptions.
    
    Layer 1: Pure taxonomy lookup (0 tokens)
    
    Returns:
        JSON string with nib types and their basic properties
    """
    result = {
        "nib_types": {
            nib_id: {
                "name": data["name"],
                "description": data["description"],
                "tine_structure": data["tine_structure"],
                "tip_geometry": data["tip_geometry"],
                "flex": data["flex_characteristics"],
                "stroke_ratio": data["stroke_width_ratio"]
            }
            for nib_id, data in NIB_TYPES.items()
        },
        "total_types": len(NIB_TYPES),
        "cost_tokens": 0
    }
    return json.dumps(result, indent=2)


@mcp.tool()
def get_nib_specifications(nib_id: str) -> str:
    """
    Get complete specifications for a specific nib type.
    
    Layer 1: Pure taxonomy lookup (0 tokens)
    
    Args:
        nib_id: Nib identifier (e.g., "pointed_flexible", "broad_edge_square")
        
    Returns:
        JSON string with complete nib specifications including visual parameters
    """
    if nib_id not in NIB_TYPES:
        available = ", ".join(NIB_TYPES.keys())
        return json.dumps({
            "error": f"Unknown nib type: {nib_id}",
            "available_types": available
        }, indent=2)
    
    nib_data = NIB_TYPES[nib_id]
    
    # Gather visual parameters
    line_quality = VISUAL_PARAMETERS["line_quality"].get(nib_id, {})
    ink_behavior = VISUAL_PARAMETERS["ink_behavior"].get(nib_id, {})
    directional = VISUAL_PARAMETERS["directional_emphasis"].get(nib_id, {})
    
    result = {
        "nib_id": nib_id,
        "physical_properties": {
            "name": nib_data["name"],
            "tine_structure": nib_data["tine_structure"],
            "material": nib_data["material"],
            "tip_geometry": nib_data["tip_geometry"],
            "flex_characteristics": nib_data["flex_characteristics"],
            "stroke_width_ratio": nib_data["stroke_width_ratio"]
        },
        "visual_characteristics": {
            "line_quality": line_quality,
            "ink_behavior": ink_behavior,
            "directional_properties": directional
        },
        "optimal_uses": nib_data["optimal_use"],
        "description": nib_data["description"],
        "cost_tokens": 0
    }
    
    return json.dumps(result, indent=2)

# ============================================================================
# LAYER 2 TOOLS: Deterministic Mapping (0 tokens)
# ============================================================================

@mcp.tool()
def map_nib_to_visual_parameters(
    nib_id: str,
    intensity: str = "moderate",
    emphasis: str = "balanced"
) -> str:
    """
    Map nib type to visual parameters for image generation.
    
    Layer 2: Deterministic operation (0 tokens)
    
    Args:
        nib_id: Nib identifier
        intensity: "subtle", "moderate", "dramatic"
        emphasis: "line_quality", "ink_flow", "directional", "balanced"
        
    Returns:
        JSON string with complete visual parameter set
    """
    if nib_id not in NIB_TYPES:
        return json.dumps({"error": f"Unknown nib type: {nib_id}"})
    
    nib_data = NIB_TYPES[nib_id]
    line_quality = VISUAL_PARAMETERS["line_quality"].get(nib_id, {})
    ink_behavior = VISUAL_PARAMETERS["ink_behavior"].get(nib_id, {})
    directional = VISUAL_PARAMETERS["directional_emphasis"].get(nib_id, {})
    
    # Intensity multipliers
    intensity_map = {
        "subtle": 0.5,
        "moderate": 1.0,
        "dramatic": 1.5
    }
    multiplier = intensity_map.get(intensity, 1.0)
    
    # Build emphasis-weighted parameters
    result = {
        "nib_id": nib_id,
        "nib_name": nib_data["name"],
        "intensity": intensity,
        "emphasis": emphasis,
        "parameters": {
            "stroke_width_ratio": nib_data["stroke_width_ratio"],
            "line_quality": line_quality,
            "ink_behavior": ink_behavior,
            "directional_properties": directional,
            "material_signature": nib_data["material"]
        },
        "visual_keywords": _extract_keywords(
            line_quality, ink_behavior, directional, emphasis
        ),
        "intensity_multiplier": multiplier,
        "methodology": "deterministic_taxonomy_mapping",
        "cost_tokens": 0
    }
    
    return json.dumps(result, indent=2)


def _extract_keywords(
    line_quality: Dict,
    ink_behavior: Dict,
    directional: Dict,
    emphasis: str
) -> List[str]:
    """Extract and weight keywords based on emphasis."""
    keywords = []
    
    if emphasis in ["line_quality", "balanced"]:
        keywords.extend(line_quality.get("keywords", []))
    
    if emphasis in ["ink_flow", "balanced"]:
        keywords.extend(ink_behavior.get("keywords", []))
    
    if emphasis in ["directional", "balanced"]:
        keywords.extend(directional.get("keywords", []))
    
    return keywords


@mcp.tool()
def analyze_nib_from_description(description: str) -> str:
    """
    Analyze text description and suggest matching nib types.
    
    Layer 2: Deterministic keyword matching (0 tokens)
    
    Args:
        description: Natural language description of desired stroke characteristics
        
    Returns:
        JSON string with ranked nib matches and confidence scores
    """
    description_lower = description.lower()
    
    # Keyword matching
    matches = []
    for nib_id, nib_data in NIB_TYPES.items():
        score = 0
        matched_keywords = []
        
        # Check description
        if any(word in description_lower for word in nib_data["description"].lower().split()):
            score += 2
            matched_keywords.append("description_match")
        
        # Check optimal uses
        for use in nib_data["optimal_use"]:
            if use.replace("_", " ") in description_lower:
                score += 3
                matched_keywords.append(f"use:{use}")
        
        # Check visual keywords
        line_quality = VISUAL_PARAMETERS["line_quality"].get(nib_id, {})
        for keyword in line_quality.get("keywords", []):
            if keyword.lower() in description_lower:
                score += 1
                matched_keywords.append(f"visual:{keyword}")
        
        if score > 0:
            matches.append({
                "nib_id": nib_id,
                "nib_name": nib_data["name"],
                "confidence_score": score,
                "matched_keywords": matched_keywords
            })
    
    # Sort by confidence
    matches.sort(key=lambda x: x["confidence_score"], reverse=True)
    
    result = {
        "description": description,
        "matches": matches[:5],  # Top 5
        "methodology": "keyword_matching",
        "cost_tokens": 0
    }
    
    return json.dumps(result, indent=2)

# ============================================================================
# LAYER 3 TOOLS: Synthesis Interface (Minimal tokens)
# ============================================================================

@mcp.tool()
def generate_nib_stroke_prompt(
    nib_id: str,
    intensity: str = "moderate",
    emphasis: str = "balanced",
    style_modifier: str = ""
) -> str:
    """
    Generate image generation prompt for nib stroke characteristics.
    
    Layer 3: Interface for LLM synthesis (minimal tokens)
    
    Args:
        nib_id: Nib identifier
        intensity: "subtle", "moderate", "dramatic"
        emphasis: "line_quality", "ink_flow", "directional", "balanced"
        style_modifier: Optional style prefix (e.g., "photorealistic", "abstract")
        
    Returns:
        JSON string with prompt and parameters for image generation
    """
    # Get deterministic parameters (Layer 2)
    params_json = map_nib_to_visual_parameters(nib_id, intensity, emphasis)
    params = json.loads(params_json)
    
    if "error" in params:
        return params_json
    
    # Build prompt from keywords
    keywords = params["visual_keywords"]
    nib_name = params["nib_name"]
    
    # Construct prompt
    prompt_parts = []
    
    if style_modifier:
        prompt_parts.append(style_modifier)
    
    prompt_parts.append(f"{nib_name} calligraphy stroke")
    prompt_parts.extend(keywords[:8])  # Limit to top keywords
    
    prompt = ", ".join(prompt_parts)
    
    result = {
        "prompt": prompt,
        "nib_id": nib_id,
        "nib_name": nib_name,
        "parameters": params["parameters"],
        "intensity": intensity,
        "emphasis": emphasis,
        "style_modifier": style_modifier,
        "methodology": "deterministic_parameter_to_prompt",
        "cost_tokens": 0
    }
    
    return json.dumps(result, indent=2)


@mcp.tool()
def compare_nib_characteristics(nib_id_1: str, nib_id_2: str) -> str:
    """
    Compare visual characteristics between two nib types.
    
    Layer 2: Deterministic comparison (0 tokens)
    
    Args:
        nib_id_1: First nib identifier
        nib_id_2: Second nib identifier
        
    Returns:
        JSON string with comparative analysis
    """
    if nib_id_1 not in NIB_TYPES or nib_id_2 not in NIB_TYPES:
        return json.dumps({"error": "One or both nib types not found"})
    
    nib_1 = NIB_TYPES[nib_id_1]
    nib_2 = NIB_TYPES[nib_id_2]
    
    line_1 = VISUAL_PARAMETERS["line_quality"].get(nib_id_1, {})
    line_2 = VISUAL_PARAMETERS["line_quality"].get(nib_id_2, {})
    
    result = {
        "comparison": {
            "nib_1": {
                "id": nib_id_1,
                "name": nib_1["name"],
                "flex": nib_1["flex_characteristics"],
                "geometry": nib_1["tip_geometry"],
                "stroke_ratio": nib_1["stroke_width_ratio"],
                "stroke_dynamics": line_1.get("stroke_dynamics"),
                "edge_char": line_1.get("edge_characteristics")
            },
            "nib_2": {
                "id": nib_id_2,
                "name": nib_2["name"],
                "flex": nib_2["flex_characteristics"],
                "geometry": nib_2["tip_geometry"],
                "stroke_ratio": nib_2["stroke_width_ratio"],
                "stroke_dynamics": line_2.get("stroke_dynamics"),
                "edge_char": line_2.get("edge_characteristics")
            }
        },
        "differences": {
            "flex": nib_1["flex_characteristics"] != nib_2["flex_characteristics"],
            "geometry": nib_1["tip_geometry"] != nib_2["tip_geometry"],
            "material": nib_1["material"] != nib_2["material"]
        },
        "cost_tokens": 0
    }
    
    return json.dumps(result, indent=2)


# ============================================================================
# PHASE 1A: TRAJECTORY COMPUTATION (Layer 2 - 0 tokens)
# ============================================================================

def _state_to_vector(state_id: str) -> np.ndarray:
    """Convert state ID to 5D numpy vector."""
    coords = CALLIGRAPHY_COORDS[state_id]
    return np.array([coords[p] for p in CALLIGRAPHY_PARAMETER_NAMES])


def _vector_to_state(vec: np.ndarray) -> dict:
    """Convert 5D numpy vector to state dict."""
    return {p: float(np.clip(vec[i], 0.0, 1.0))
            for i, p in enumerate(CALLIGRAPHY_PARAMETER_NAMES)}


def _generate_oscillation(num_steps: int, num_cycles: float,
                          pattern: str) -> np.ndarray:
    """Generate oscillation waveform returning values in [0, 1]."""
    t = np.linspace(0, 2 * math.pi * num_cycles, num_steps, endpoint=False)

    if pattern == "sinusoidal":
        return 0.5 * (1.0 + np.sin(t))
    elif pattern == "triangular":
        t_norm = (t / (2 * math.pi)) % 1.0
        return np.where(t_norm < 0.5, 2.0 * t_norm, 2.0 * (1.0 - t_norm))
    elif pattern == "square":
        t_norm = (t / (2 * math.pi)) % 1.0
        return np.where(t_norm < 0.5, 0.0, 1.0)
    else:
        raise ValueError(f"Unknown pattern: {pattern}")


def _generate_preset_trajectory(preset_config: dict) -> List[dict]:
    """Generate full trajectory for a Phase 2.6 preset as list of state dicts."""
    vec_a = _state_to_vector(preset_config["state_a"])
    vec_b = _state_to_vector(preset_config["state_b"])

    total_steps = preset_config["num_cycles"] * preset_config["steps_per_cycle"]
    alpha = _generate_oscillation(
        total_steps, preset_config["num_cycles"], preset_config["pattern"]
    )

    trajectory = []
    for a in alpha:
        vec = (1.0 - a) * vec_a + a * vec_b
        trajectory.append(_vector_to_state(vec))
    return trajectory


@mcp.tool()
def compute_calligraphy_trajectory(
    start_state: str,
    end_state: str,
    num_steps: int = 20
) -> str:
    """
    Compute smooth trajectory between two calligraphy nib states.

    Layer 2: Deterministic interpolation (0 tokens).

    Args:
        start_state: Starting nib state ID (e.g. "pointed_flexible")
        end_state: Target nib state ID (e.g. "broad_edge_square")
        num_steps: Number of interpolation steps (default 20)

    Returns:
        JSON with trajectory as list of 5D state dicts, plus metadata.
    """
    if start_state not in CALLIGRAPHY_COORDS:
        return json.dumps({"error": f"Unknown state: {start_state}",
                           "available": list(CALLIGRAPHY_COORDS.keys())})
    if end_state not in CALLIGRAPHY_COORDS:
        return json.dumps({"error": f"Unknown state: {end_state}",
                           "available": list(CALLIGRAPHY_COORDS.keys())})

    vec_a = _state_to_vector(start_state)
    vec_b = _state_to_vector(end_state)

    trajectory = []
    for i in range(num_steps):
        t = i / max(num_steps - 1, 1)
        vec = (1.0 - t) * vec_a + t * vec_b
        trajectory.append(_vector_to_state(vec))

    distance = float(np.linalg.norm(vec_b - vec_a))

    return json.dumps({
        "start_state": start_state,
        "end_state": end_state,
        "num_steps": num_steps,
        "euclidean_distance": round(distance, 4),
        "trajectory": trajectory,
        "parameter_names": CALLIGRAPHY_PARAMETER_NAMES,
        "cost_tokens": 0
    }, indent=2)


@mcp.tool()
def compute_calligraphy_distance(state_a: str, state_b: str) -> str:
    """
    Compute Euclidean distance between two nib states in 5D parameter space.

    Layer 2: Deterministic computation (0 tokens).

    Args:
        state_a: First nib state ID
        state_b: Second nib state ID

    Returns:
        JSON with distance and per-parameter differences.
    """
    if state_a not in CALLIGRAPHY_COORDS or state_b not in CALLIGRAPHY_COORDS:
        return json.dumps({"error": "Unknown state ID",
                           "available": list(CALLIGRAPHY_COORDS.keys())})

    va = _state_to_vector(state_a)
    vb = _state_to_vector(state_b)
    diff = vb - va

    return json.dumps({
        "state_a": state_a,
        "state_b": state_b,
        "euclidean_distance": round(float(np.linalg.norm(diff)), 4),
        "per_parameter": {
            p: round(float(diff[i]), 4)
            for i, p in enumerate(CALLIGRAPHY_PARAMETER_NAMES)
        },
        "cost_tokens": 0
    }, indent=2)


# ============================================================================
# PHASE 2.6 TOOLS: RHYTHMIC COMPOSITION (Layer 2 - 0 tokens)
# ============================================================================

@mcp.tool()
def list_calligraphy_rhythmic_presets() -> str:
    """
    List all Phase 2.6 rhythmic presets for calligraphy nib aesthetics.

    Layer 1: Pure taxonomy lookup (0 tokens).

    Returns:
        JSON with all preset names, periods, patterns, and descriptions.
    """
    presets = {}
    for name, cfg in CALLIGRAPHY_RHYTHMIC_PRESETS.items():
        presets[name] = {
            "state_a": cfg["state_a"],
            "state_b": cfg["state_b"],
            "pattern": cfg["pattern"],
            "steps_per_cycle": cfg["steps_per_cycle"],
            "num_cycles": cfg["num_cycles"],
            "total_steps": cfg["num_cycles"] * cfg["steps_per_cycle"],
            "description": cfg["description"]
        }

    return json.dumps({
        "presets": presets,
        "total_presets": len(presets),
        "period_landscape": sorted(set(
            c["steps_per_cycle"] for c in CALLIGRAPHY_RHYTHMIC_PRESETS.values()
        )),
        "cost_tokens": 0
    }, indent=2)


@mcp.tool()
def apply_calligraphy_rhythmic_preset(preset_name: str) -> str:
    """
    Generate a complete oscillation sequence for a calligraphy rhythmic preset.

    Layer 2: Deterministic sequence generation (0 tokens).
    Generates trajectory over one full period (steps_per_cycle steps).

    Args:
        preset_name: Preset identifier (e.g. "pressure_swell_cycle")

    Returns:
        JSON with one-period trajectory, state endpoints, and metadata.
    """
    if preset_name not in CALLIGRAPHY_RHYTHMIC_PRESETS:
        return json.dumps({
            "error": f"Unknown preset: {preset_name}",
            "available": list(CALLIGRAPHY_RHYTHMIC_PRESETS.keys())
        })

    cfg = CALLIGRAPHY_RHYTHMIC_PRESETS[preset_name]
    vec_a = _state_to_vector(cfg["state_a"])
    vec_b = _state_to_vector(cfg["state_b"])

    # Generate ONE period
    period = cfg["steps_per_cycle"]
    alpha = _generate_oscillation(period, 1, cfg["pattern"])

    sequence = []
    for i, a in enumerate(alpha):
        vec = (1.0 - a) * vec_a + a * vec_b
        state = _vector_to_state(vec)
        sequence.append({
            "step": i,
            "phase_pct": round(100.0 * i / period, 1),
            "state": state
        })

    return json.dumps({
        "preset_name": preset_name,
        "description": cfg["description"],
        "period": period,
        "pattern": cfg["pattern"],
        "state_a": cfg["state_a"],
        "state_b": cfg["state_b"],
        "sequence": sequence,
        "parameter_names": CALLIGRAPHY_PARAMETER_NAMES,
        "cost_tokens": 0
    }, indent=2)


@mcp.tool()
def generate_calligraphy_rhythmic_composition(
    preset_name: str,
    num_cycles: Optional[int] = None
) -> str:
    """
    Generate multi-cycle rhythmic composition from a calligraphy preset.

    Layer 2: Deterministic composition (0 tokens).
    Returns full multi-cycle trajectory suitable for animation keyframes
    or temporal aesthetic workflows.

    Args:
        preset_name: Preset identifier
        num_cycles: Override number of cycles (default: use preset value)

    Returns:
        JSON with full trajectory, cycle boundaries, and composition metadata.
    """
    if preset_name not in CALLIGRAPHY_RHYTHMIC_PRESETS:
        return json.dumps({
            "error": f"Unknown preset: {preset_name}",
            "available": list(CALLIGRAPHY_RHYTHMIC_PRESETS.keys())
        })

    cfg = CALLIGRAPHY_RHYTHMIC_PRESETS[preset_name]
    cycles = num_cycles if num_cycles is not None else cfg["num_cycles"]
    period = cfg["steps_per_cycle"]
    total_steps = cycles * period

    full_cfg = {**cfg, "num_cycles": cycles}
    trajectory = _generate_preset_trajectory(full_cfg)

    # Mark cycle boundaries
    cycle_boundaries = [i * period for i in range(cycles + 1)]

    return json.dumps({
        "preset_name": preset_name,
        "description": cfg["description"],
        "period": period,
        "num_cycles": cycles,
        "total_steps": total_steps,
        "pattern": cfg["pattern"],
        "cycle_boundaries": cycle_boundaries,
        "trajectory": trajectory,
        "parameter_names": CALLIGRAPHY_PARAMETER_NAMES,
        "cost_tokens": 0
    }, indent=2)


# ============================================================================
# PHASE 2.7: ATTRACTOR VISUALIZATION PROMPT GENERATION
# ============================================================================

def _extract_visual_vocabulary_from_coords(
    state: dict,
    strength: float = 1.0
) -> dict:
    """
    Extract nearest visual type and keywords from 5D coordinates.

    Nearest-neighbor lookup against CALLIGRAPHY_VISUAL_TYPES.

    Args:
        state: Dict with calligraphy parameter values
        strength: Weight multiplier for keyword relevance [0.0, 1.0]

    Returns:
        Dict with nearest_type, distance, keywords, optical_properties, colors
    """
    state_vec = np.array([state.get(p, 0.5) for p in CALLIGRAPHY_PARAMETER_NAMES])

    best_type = None
    best_dist = float("inf")

    for type_id, vtype in CALLIGRAPHY_VISUAL_TYPES.items():
        type_vec = np.array([vtype["coords"][p] for p in CALLIGRAPHY_PARAMETER_NAMES])
        dist = float(np.linalg.norm(state_vec - type_vec))
        if dist < best_dist:
            best_dist = dist
            best_type = type_id

    vt = CALLIGRAPHY_VISUAL_TYPES[best_type]
    return {
        "nearest_type": best_type,
        "distance": round(best_dist, 4),
        "strength": strength,
        "keywords": vt["keywords"],
        "optical_properties": vt["optical_properties"],
        "color_associations": vt["color_associations"]
    }


@mcp.tool()
def get_calligraphy_visual_types() -> str:
    """
    List all calligraphy visual types with keywords and optical properties.

    Layer 1: Pure taxonomy lookup (0 tokens).

    Returns:
        JSON catalog of visual types with coordinates, keywords,
        optical properties, and color associations.
    """
    catalog = {}
    for type_id, vt in CALLIGRAPHY_VISUAL_TYPES.items():
        catalog[type_id] = {
            "coordinates": vt["coords"],
            "keywords": vt["keywords"],
            "optical_properties": vt["optical_properties"],
            "color_associations": vt["color_associations"]
        }

    return json.dumps({
        "visual_types": catalog,
        "total_types": len(catalog),
        "parameter_names": CALLIGRAPHY_PARAMETER_NAMES,
        "cost_tokens": 0
    }, indent=2)


@mcp.tool()
def generate_calligraphy_attractor_prompt(
    state: str,
    mode: str = "composite",
    style_modifier: str = ""
) -> str:
    """
    Generate image-generation prompt from calligraphy 5D coordinates or state ID.

    Layer 2: Deterministic vocabulary extraction (0 tokens).

    Maps a point in calligraphy parameter space to the nearest visual type
    and assembles an image-generation-ready prompt from its vocabulary.

    Args:
        state: Either a nib state ID (e.g. "copperplate_gold") or a JSON
               string of raw coordinates {"stroke_contrast": 0.7, ...}
        mode: "composite" (single blended prompt) or "descriptive"
              (structured breakdown with optical properties)
        style_modifier: Optional prefix (e.g. "photorealistic macro",
                        "abstract ink wash")

    Returns:
        JSON with assembled prompt, visual type match, and full metadata.
    """
    # Parse state: either an ID or raw coordinates
    if state in CALLIGRAPHY_COORDS:
        coords = CALLIGRAPHY_COORDS[state]
        state_label = state
    else:
        try:
            coords = json.loads(state)
            state_label = "custom_coordinates"
        except (json.JSONDecodeError, TypeError):
            return json.dumps({
                "error": f"State must be a nib ID or JSON coordinate dict. "
                         f"Available IDs: {list(CALLIGRAPHY_COORDS.keys())}"
            })

    vocab = _extract_visual_vocabulary_from_coords(coords, strength=1.0)

    if mode == "composite":
        parts = []
        if style_modifier:
            parts.append(style_modifier)
        parts.extend(vocab["keywords"])
        parts.extend(vocab["color_associations"][:2])
        prompt = ", ".join(parts)
    elif mode == "descriptive":
        sections = {
            "visual_character": ", ".join(vocab["keywords"][:3]),
            "stroke_quality": ", ".join(vocab["keywords"][3:]),
            "surface": vocab["optical_properties"]["surface_quality"],
            "light": vocab["optical_properties"]["light_interaction"],
            "depth": vocab["optical_properties"]["depth_cue"],
            "palette": ", ".join(vocab["color_associations"])
        }
        prompt = " | ".join(f"{k}: {v}" for k, v in sections.items())
        if style_modifier:
            prompt = f"{style_modifier} | {prompt}"
    else:
        return json.dumps({"error": f"Unknown mode: {mode}. Use 'composite' or 'descriptive'."})

    return json.dumps({
        "prompt": prompt,
        "state": state_label,
        "coordinates": coords,
        "nearest_visual_type": vocab["nearest_type"],
        "type_distance": vocab["distance"],
        "keywords": vocab["keywords"],
        "optical_properties": vocab["optical_properties"],
        "color_associations": vocab["color_associations"],
        "mode": mode,
        "parameter_names": CALLIGRAPHY_PARAMETER_NAMES,
        "cost_tokens": 0
    }, indent=2)


@mcp.tool()
def generate_calligraphy_sequence_prompts(
    preset_name: str,
    num_keyframes: int = 8
) -> str:
    """
    Generate a sequence of image prompts along a rhythmic preset trajectory.

    Layer 2: Deterministic vocabulary extraction (0 tokens).

    Samples evenly-spaced keyframes from one period of the preset and
    generates an attractor visualization prompt for each, suitable for
    animation workflows or ComfyUI batch processing.

    Args:
        preset_name: Rhythmic preset identifier
        num_keyframes: Number of keyframes to extract (default 8)

    Returns:
        JSON with ordered keyframe prompts, visual type transitions,
        and composition metadata.
    """
    if preset_name not in CALLIGRAPHY_RHYTHMIC_PRESETS:
        return json.dumps({
            "error": f"Unknown preset: {preset_name}",
            "available": list(CALLIGRAPHY_RHYTHMIC_PRESETS.keys())
        })

    cfg = CALLIGRAPHY_RHYTHMIC_PRESETS[preset_name]
    period = cfg["steps_per_cycle"]

    # Generate one period of the preset
    one_cycle_cfg = {**cfg, "num_cycles": 1}
    trajectory = _generate_preset_trajectory(one_cycle_cfg)

    # Sample keyframes evenly
    indices = [int(round(i * (period - 1) / max(num_keyframes - 1, 1)))
               for i in range(num_keyframes)]

    keyframes = []
    for kf_idx, traj_idx in enumerate(indices):
        state = trajectory[traj_idx]
        vocab = _extract_visual_vocabulary_from_coords(state)

        keyframes.append({
            "keyframe": kf_idx,
            "trajectory_step": traj_idx,
            "phase_pct": round(100.0 * traj_idx / period, 1),
            "nearest_visual_type": vocab["nearest_type"],
            "type_distance": vocab["distance"],
            "prompt": ", ".join(vocab["keywords"]),
            "color_associations": vocab["color_associations"],
            "coordinates": state
        })

    # Detect visual type transitions across keyframes
    type_sequence = [kf["nearest_visual_type"] for kf in keyframes]
    unique_types = list(dict.fromkeys(type_sequence))  # ordered unique

    return json.dumps({
        "preset_name": preset_name,
        "description": cfg["description"],
        "period": period,
        "num_keyframes": num_keyframes,
        "keyframes": keyframes,
        "type_transitions": type_sequence,
        "unique_types_visited": unique_types,
        "parameter_names": CALLIGRAPHY_PARAMETER_NAMES,
        "cost_tokens": 0
    }, indent=2)


# ============================================================================
# TIER 4D: DOMAIN REGISTRY CONFIGURATION
# ============================================================================

@mcp.tool()
def get_domain_registry_config() -> str:
    """
    Return Tier 4D integration configuration for compositional limit cycles.

    Layer 2: Pure lookup (0 tokens).

    Returns the domain signature for registering calligraphy-nib with
    aesthetic-dynamics-core multi-domain composition.
    """
    return json.dumps({
        "domain_id": "calligraphy",
        "display_name": "Calligraphy Nib Aesthetics",
        "mcp_server": "calligraphy-nib",
        "parameter_names": CALLIGRAPHY_PARAMETER_NAMES,
        "n_parameters": len(CALLIGRAPHY_PARAMETER_NAMES),
        "state_coordinates": CALLIGRAPHY_COORDS,
        "n_states": len(CALLIGRAPHY_COORDS),
        "presets": {
            name: {
                "period": cfg["steps_per_cycle"],
                "pattern": cfg["pattern"],
                "state_a": cfg["state_a"],
                "state_b": cfg["state_b"],
                "description": cfg["description"]
            }
            for name, cfg in CALLIGRAPHY_RHYTHMIC_PRESETS.items()
        },
        "period_landscape": sorted(set(
            c["steps_per_cycle"] for c in CALLIGRAPHY_RHYTHMIC_PRESETS.values()
        )),
        "visual_types": {
            vt_id: {
                "coords": vt["coords"],
                "n_keywords": len(vt["keywords"])
            }
            for vt_id, vt in CALLIGRAPHY_VISUAL_TYPES.items()
        },
        "n_visual_types": len(CALLIGRAPHY_VISUAL_TYPES),
        "integration_notes": (
            "Period landscape [11, 14, 18, 22, 28] selected for cross-domain "
            "resonance: 18 shared with nuclear/catastrophe/diatom, 22 shared "
            "with catastrophe/heraldic, 28 resonates with composite beat "
            "mechanism. Prime period 11 adds beat complexity."
        ),
        "cost_tokens": 0
    }, indent=2)


# ============================================================================
# SERVER INFO
# ============================================================================

@mcp.tool()
def get_server_info() -> str:
    """
    Get information about the Calligraphy Nib Visual Vocabulary MCP server.
    
    Returns server metadata, capabilities, and usage guidance.
    """
    info = {
        "name": "Calligraphy Nib Visual Vocabulary",
        "version": "2.0.0",
        "architecture": "three_layer_olog",
        "description": (
            "Deterministic nib→visual parameter mapping for image synthesis "
            "with Phase 2.6 rhythmic composition and Phase 2.7 attractor "
            "visualization prompt generation"
        ),
        "capabilities": {
            "nib_types": len(NIB_TYPES),
            "visual_parameters": list(VISUAL_PARAMETERS.keys()),
            "layer_1_tools": [
                "list_nib_types",
                "get_nib_specifications",
                "list_calligraphy_rhythmic_presets",
                "get_calligraphy_visual_types"
            ],
            "layer_2_tools": [
                "map_nib_to_visual_parameters",
                "analyze_nib_from_description",
                "compare_nib_characteristics",
                "compute_calligraphy_trajectory",
                "compute_calligraphy_distance",
                "apply_calligraphy_rhythmic_preset",
                "generate_calligraphy_rhythmic_composition",
                "generate_calligraphy_attractor_prompt",
                "generate_calligraphy_sequence_prompts",
                "get_domain_registry_config"
            ],
            "layer_3_tools": ["generate_nib_stroke_prompt"]
        },
        "phase_2_6_enhancements": {
            "rhythmic_composition": True,
            "parameter_space": "5D normalized [0.0, 1.0]",
            "parameter_names": CALLIGRAPHY_PARAMETER_NAMES,
            "n_canonical_states": len(CALLIGRAPHY_COORDS),
            "n_presets": len(CALLIGRAPHY_RHYTHMIC_PRESETS),
            "period_landscape": sorted(set(
                c["steps_per_cycle"]
                for c in CALLIGRAPHY_RHYTHMIC_PRESETS.values()
            )),
            "presets": {
                name: {
                    "period": cfg["steps_per_cycle"],
                    "pattern": cfg["pattern"],
                    "states": f"{cfg['state_a']} ↔ {cfg['state_b']}"
                }
                for name, cfg in CALLIGRAPHY_RHYTHMIC_PRESETS.items()
            }
        },
        "phase_2_7_enhancements": {
            "attractor_visualization": True,
            "visual_types": list(CALLIGRAPHY_VISUAL_TYPES.keys()),
            "n_visual_types": len(CALLIGRAPHY_VISUAL_TYPES),
            "prompt_modes": ["composite", "descriptive"],
            "sequence_generation": True
        },
        "tier_4d_integration": {
            "domain_registry": True,
            "domain_id": "calligraphy",
            "compositional_limit_cycles": True,
            "cross_domain_resonances": [
                "Period 18: shared with nuclear, catastrophe, diatom",
                "Period 22: shared with catastrophe, heraldic",
                "Period 28: resonates with composite beat mechanism"
            ]
        },
        "cost_profile": {
            "layer_1_operations": "0 tokens (pure taxonomy lookup)",
            "layer_2_operations": "0 tokens (deterministic mapping)",
            "layer_3_operations": "minimal tokens (synthesis interface)",
            "total_savings_vs_pure_llm": "~85%"
        },
        "workflow": {
            "1_discover": "list_nib_types() → see available nibs",
            "2_specify": "get_nib_specifications(nib_id) → full details",
            "3_map": "map_nib_to_visual_parameters(nib_id) → image params",
            "4_generate": "generate_nib_stroke_prompt(nib_id) → prompt text",
            "5_rhythm": "apply_calligraphy_rhythmic_preset(name) → temporal composition",
            "6_visualize": "generate_calligraphy_attractor_prompt(state) → attractor prompt",
            "7_sequence": "generate_calligraphy_sequence_prompts(name) → animation keyframes",
            "8_compose": "get_domain_registry_config() → Tier 4D multi-domain integration"
        },
        "nib_categories": {
            "pointed_nibs": ["pointed_flexible", "pointed_rigid", "copperplate_gold", "scroll_nib"],
            "broad_edge_nibs": ["broad_edge_square", "broad_edge_stub", "oblique_left", "oblique_right"],
            "specialty_nibs": ["monoline_round", "glass_dip"]
        }
    }
    
    return json.dumps(info, indent=2)

if __name__ == "__main__":
    mcp.run()
