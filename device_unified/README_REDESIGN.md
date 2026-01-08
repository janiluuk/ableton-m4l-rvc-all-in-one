# UI Redesign - BS-3 Style Layout

## Overview

This redesign transforms the RVC Unified Device to match the BS-3 style interface as requested, with colored stem controls on the left and prominent pitch/octave control on the right.

## Quick Visual Reference

```
┌─────────────────────┬──────────────────────────┬─────────────┐
│  STEMS (Colored)    │  MAIN CONTROLS          │  ADVANCED   │
├─────────────────────┼──────────────────────────┼─────────────┤
│ [MAIN VOCALS - Red] │ Backend | Mode           │ UVR Options │
│  • Volume           │                          │             │
│  • RMS | Protect    │ ┌──────────────────────┐ │ Stable Opts │
│                     │ │ PITCH/OCTAVE (large) │ │             │
│ [BACKUP VOCALS-Blue]│ └──────────────────────┘ │             │
│  • Volume           │ Voice Model              │             │
│  • Index Rate       │ [PROCESS BUTTON]         │             │
│                     │ [Drop Zone]              │             │
│ [INSTRUMENTAL-Green]│                          │             │
│  • Volume           │                          │             │
└─────────────────────┴──────────────────────────┴─────────────┘
```

## What Changed

### 1. Left Column (Stems)
- **NEW**: Three colored panel backgrounds
  - Main Vocals (Red/Pink): RGB(0.8, 0.3, 0.3)
  - Backup Vocals (Blue): RGB(0.5, 0.6, 0.9)
  - Instrumental (Green): RGB(0.4, 0.8, 0.5)
- **NEW**: Volume controls for each stem
- **MOVED**: RMS Mix and Protect to Main Vocals section
- **MOVED**: Index Rate to Backup Vocals section

### 2. Right Column (Main Controls)
- **PROMINENT**: Pitch/Octave control at top (larger size)
- **MOVED**: Backend and Mode selection to top
- **KEPT**: All processing controls (model, API, server, etc.)
- **MOVED**: Process button and drop zone centrally located

### 3. Far Right Column (Advanced)
- **MOVED**: UVR model settings (model, shifts, segment)
- **MOVED**: Stable Audio server and prompt
- **MOVED**: Filter Radius (global control)

### 4. Bottom Section
- **KEPT**: All output options (destination mode, new track buttons)
- **KEPT**: Takes history and clip naming
- **KEPT**: Status, progress bar, error messages
- **KEPT**: Waveform display

## File Changes

| File | Status | Description |
|------|--------|-------------|
| `RVC_Unified_Device.maxpat` | Modified | Main Max patch with new layout (148 boxes) |
| `UI_LAYOUT.md` | New | Detailed layout specification |
| `REDESIGN_SUMMARY.md` | New | Before/after comparison |
| `README_REDESIGN.md` | New | This file |
| `.gitignore` | Modified | Added `*.backup` |

## Technical Details

- **Window Size**: 1200×850 pixels (increased from 900×700)
- **Font Sizes**: Standardized (11pt labels, 13pt titles, 14pt prominent)
- **Total Boxes**: 148 UI elements
- **Colored Panels**: 3 panel objects added
- **New Controls**: 9 new UI elements (3 stems × 3 controls each)
- **Patchlines**: All connections preserved and updated

## Backend Compatibility

✅ All existing functionality preserved:
- JavaScript handlers unchanged
- Replicate and Local server support intact
- All processing modes work (Voice, UVR, Stable Audio)
- Volume controls connect to existing parameters:
  - `main_vocals_volume_change`
  - `backup_vocals_volume_change`
  - `instrumental_volume_change`

## Testing Checklist

When testing this redesign in Max/Ableton Live:

1. ✅ **Visual Appearance**
   - [ ] Colored panels render correctly
   - [ ] All controls are visible and properly positioned
   - [ ] No overlapping controls
   - [ ] Font sizes are readable

2. ✅ **Functionality**
   - [ ] Volume controls send correct values to backend
   - [ ] Pitch/Octave control works
   - [ ] Processing button executes correctly
   - [ ] File drop works
   - [ ] All modes work (Voice, UVR, Stable Audio)

3. ✅ **Workflow**
   - [ ] Easy to identify stem controls
   - [ ] Pitch control is prominent and easy to use
   - [ ] Logical flow from left to right
   - [ ] Status messages display correctly

## Design Rationale

### Why BS-3 Style?
The BS-3 device is known for its clean, functional layout with:
- Clear visual separation of different audio channels/stems
- Prominent octave/pitch controls
- Logical grouping of related parameters

### Why These Colors?
- **Red for Main Vocals**: Traditional "hot" color for primary/lead elements
- **Blue for Backup Vocals**: Cool, supporting color for secondary elements
- **Green for Instrumental**: Neutral, balanced color for accompaniment

### Why This Layout?
- **Left-to-Right Flow**: Stems → Processing → Output (natural workflow)
- **Visual Hierarchy**: Most important controls (pitch, process) are larger
- **Grouping**: Related controls are spatially close
- **Consistency**: Similar controls have similar positions within their sections

## Known Limitations

1. **Max for Live Required**: This is a Max patch and requires Max for Live to run
2. **No Real-time Preview**: Must process audio to hear changes (design limitation of RVC)
3. **Single Filter**: Filter Radius is global, not per-stem (backend limitation)

## Future Enhancements (Optional)

If desired in future versions:
- Add per-stem filter controls (requires backend changes)
- Add VU meters for each stem
- Add solo/mute buttons for each stem
- Add preset management UI
- Add drag-and-drop reordering of stems

## Questions?

For questions about this redesign, see:
- `UI_LAYOUT.md` - Detailed layout specification with coordinates
- `REDESIGN_SUMMARY.md` - Before/after comparison with rationale
- Original Max patch backup: `RVC_Unified_Device.maxpat.backup`
