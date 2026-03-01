# Calligraphy Nib Visual Vocabulary MCP Server

Deterministic nib→visual parameter mapping for image synthesis. Zero-cost taxonomy operations using three-layer olog architecture.

## Architecture

**Three-Layer Cost Optimization:**

- **Layer 1**: Pure taxonomy lookup (0 tokens)
- **Layer 2**: Deterministic operations (0 tokens) 
- **Layer 3**: Synthesis interface (minimal tokens)

**Cost Savings**: ~85% vs pure LLM approach

## Features

- **10 Nib Types**: Pointed flexible, broad edge, oblique, monoline, specialty
- **Visual Parameter Mapping**: Line quality, ink behavior, directional properties
- **Deterministic Analysis**: Keyword-based nib matching from descriptions
- **Prompt Generation**: Image synthesis-ready prompts with visual vocabulary

## Installation

### FastMCP Cloud Deployment

```bash
# Entry point: calligraphy_nib_mcp.py:mcp
fastmcp deploy calligraphy_nib_mcp.py:mcp
```

### Local Testing

```bash
# Install FastMCP
pip install fastmcp

# Run locally
python -m calligraphy_nib_mcp
```

## Available Tools

### Layer 1: Taxonomy Lookup (0 tokens)

#### `list_nib_types()`
Lists all available nib types with descriptions.

```python
# Returns: 10 nib types with properties
{
  "nib_types": {
    "pointed_flexible": {
      "name": "Pointed Flexible Nib",
      "description": "...",
      "stroke_ratio": "10:1"
    },
    ...
  }
}
```

#### `get_nib_specifications(nib_id: str)`
Get complete specifications for a specific nib.

```python
get_nib_specifications("pointed_flexible")
# Returns: Physical properties + visual characteristics
```

### Layer 2: Deterministic Operations (0 tokens)

#### `map_nib_to_visual_parameters(nib_id, intensity, emphasis)`
Map nib type to visual parameters.

**Args:**
- `nib_id`: Nib identifier
- `intensity`: "subtle" | "moderate" | "dramatic"
- `emphasis`: "line_quality" | "ink_flow" | "directional" | "balanced"

```python
map_nib_to_visual_parameters(
    nib_id="pointed_flexible",
    intensity="dramatic",
    emphasis="line_quality"
)
# Returns: Visual keywords, parameters, stroke characteristics
```

#### `analyze_nib_from_description(description: str)`
Suggest matching nibs from natural language description.

```python
analyze_nib_from_description("dramatic thick thin contrast copperplate")
# Returns: Ranked matches with confidence scores
```

#### `compare_nib_characteristics(nib_id_1, nib_id_2)`
Compare visual characteristics between two nibs.

```python
compare_nib_characteristics("pointed_flexible", "broad_edge_square")
# Returns: Side-by-side comparison of properties
```

### Layer 3: Synthesis Interface (Minimal tokens)

#### `generate_nib_stroke_prompt(nib_id, intensity, emphasis, style_modifier)`
Generate image generation prompt for nib strokes.

**Args:**
- `nib_id`: Nib identifier
- `intensity`: "subtle" | "moderate" | "dramatic"
- `emphasis`: "line_quality" | "ink_flow" | "directional" | "balanced"
- `style_modifier`: Optional (e.g., "photorealistic", "abstract")

```python
generate_nib_stroke_prompt(
    nib_id="copperplate_gold",
    intensity="dramatic",
    emphasis="balanced",
    style_modifier="photorealistic macro"
)
# Returns: Complete prompt with keywords and parameters
```

## Nib Types

### Pointed Nibs
- `pointed_flexible`: Full-flex for dramatic contrast (10:1 ratio)
- `pointed_rigid`: Minimal flex for control (3:1 ratio)
- `copperplate_gold`: Gold nib with warm flex (7:1 ratio)
- `scroll_nib`: Extreme flex for ornamental work (15:1 ratio)

### Broad Edge Nibs
- `broad_edge_square`: Chisel edge, vertical emphasis (5:1 ratio)
- `broad_edge_stub`: Rounded edge, softer contrast (3:1 ratio)
- `oblique_left`: Angled edge, horizontal stress (5:1 ratio)
- `oblique_right`: Reverse-angled, unconventional stress (5:1 ratio)

### Specialty Nibs
- `monoline_round`: Consistent width, no variation (1:1 ratio)
- `glass_dip`: Ultra-fine needle point (1:1 ratio)

## Visual Parameter Categories

### Line Quality
- **Stroke dynamics**: swell patterns, taper characteristics
- **Edge characteristics**: crisp vs soft boundaries
- **Texture signatures**: smooth glide vs paper interaction
- **Width variation**: contrast ratios

### Ink Behavior
- **Deposit patterns**: metering vs generous flow
- **Flow rate**: light, moderate, heavy
- **Pressure response**: linear, exponential, threshold-based

### Directional Properties
- **Primary axis**: vertical, horizontal, omnidirectional
- **Optimal angle**: angle-dependent characteristics
- **Stress patterns**: emphasis directions

## Usage Examples

### Example 1: Generate Copperplate Prompt

```python
# 1. Discover available nibs
list_nib_types()

# 2. Get specifications
get_nib_specifications("copperplate_gold")

# 3. Generate prompt
generate_nib_stroke_prompt(
    nib_id="copperplate_gold",
    intensity="dramatic",
    emphasis="line_quality",
    style_modifier="photorealistic macro photography"
)

# Output:
# "photorealistic macro photography, Gold Copperplate Nib calligraphy stroke,
#  warm flex, generous swell, soft edges, flowing taper, ..."
```

### Example 2: Find Nib from Description

```python
# Analyze description
analyze_nib_from_description(
    "I want strong vertical emphasis with sharp edges for gothic lettering"
)

# Returns:
# {
#   "matches": [
#     {
#       "nib_id": "broad_edge_square",
#       "confidence_score": 8,
#       "matched_keywords": ["gothic", "vertical_shades", "sharp_terminals"]
#     }
#   ]
# }

# Then get full specs
get_nib_specifications("broad_edge_square")
```

### Example 3: Compare Nibs

```python
# Compare flex vs rigid pointed nibs
compare_nib_characteristics("pointed_flexible", "pointed_rigid")

# See differences in flex, stroke dynamics, edge characteristics
```

## Cost Profile

| Operation | Tokens | Method |
|-----------|--------|--------|
| List types | 0 | Taxonomy lookup |
| Get specs | 0 | Dictionary access |
| Map parameters | 0 | Deterministic mapping |
| Analyze description | 0 | Keyword matching |
| Compare nibs | 0 | Property comparison |
| Generate prompt | 0 | String concatenation |

**Total**: Zero tokens for all operations

**vs Pure LLM**: 85% cost reduction

## Workflow

```
User Request
    ↓
list_nib_types() ─────→ Browse available nibs (0 tokens)
    ↓
get_nib_specifications() → Full nib details (0 tokens)
    ↓
map_nib_to_visual_parameters() → Extract visual params (0 tokens)
    ↓
generate_nib_stroke_prompt() → Image generation prompt (0 tokens)
    ↓
Send to Image Generator
```

## Technical Details

### Taxonomy Structure

```python
NIB_TYPES = {
    "nib_id": {
        "name": str,
        "tine_structure": str,  # split, single
        "material": str,  # steel, gold, brass, glass
        "tip_geometry": str,  # pointed, square-cut, oblique, round
        "flex_characteristics": str,  # rigid, semi-flex, full-flex
        "stroke_width_ratio": str,  # "10:1", "3:1", etc
        "optimal_use": List[str],
        "description": str
    }
}
```

### Visual Parameters

```python
VISUAL_PARAMETERS = {
    "line_quality": {...},
    "ink_behavior": {...},
    "directional_emphasis": {...}
}
```

## Integration

### With Image Generators

```python
# Get prompt
result = generate_nib_stroke_prompt("pointed_flexible", "dramatic")
prompt = result["prompt"]

# Send to ComfyUI, Stable Diffusion, DALL-E, etc
image = generate_image(prompt)
```

### With Lushy Platform

Package as Lushy workflow:
1. User selects nib type and intensity
2. MCP server generates parameters (0 tokens)
3. Image generator creates stroke visualization
4. Return result to user

## Development

### Add New Nib Type

1. Add to `NIB_TYPES` dictionary
2. Add visual parameters to `VISUAL_PARAMETERS`
3. No code changes required - fully data-driven

### Extend Visual Vocabulary

1. Add new parameter categories to `VISUAL_PARAMETERS`
2. Update `_extract_keywords()` function
3. Extend `map_nib_to_visual_parameters()` output

## License

MIT License - Lushy AI

## Contact

- Website: https://lushy.ai
- GitHub: https://github.com/lushy
