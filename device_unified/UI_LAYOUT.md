# RVC Unified Device - New UI Layout (BS-3 Style)

## Layout Overview

The device has been redesigned to match the BS-3 style interface with:
- **Left side**: Stem controls in colored panels
- **Right side**: Main processing controls with pitch/octave prominently displayed

## Layout Sections

### Left Column (15-355px): Stem Controls in Colored Panels

#### Main Vocals Panel (Red/Pink) - Y: 15-185
- **MAIN VOCALS** (title)
- Volume (dB) control
- Filter control
- RMS Mix control
- Protect control

#### Backup Vocals Panel (Blue) - Y: 195-365
- **BACKUP VOCALS** (title)
- Volume (dB) control
- Index Rate control

#### Instrumental Panel (Green) - Y: 375-545
- **INSTRUMENTAL** (title)
- Volume (dB) control
- Filter Radius control

### Right Column (370-950px): Main Processing Controls

#### Top Right Section (Y: 20-150)
- Backend selection (Local/Replicate)
- Processing Mode (Voice/RVC, UVR, Stable Audio)
- **PITCH/OCTAVE** control (large, prominent - semitones adjustment)
- Pitch Algorithm selection

#### Middle Right Section (Y: 160-375)
- Voice Model selection
- Output Format
- Replicate API Key
- Local Server URL
- Custom Model URL
- **Process Button** (large, prominent)

#### Drop Zone (Y: 440-540)
- File drop area for source audio

### Far Right Column (750-950px): Advanced Controls

#### UVR Controls (Y: 20-125)
- UVR Model selection
- UVR Shifts control
- UVR Segment control

#### Stable Audio Controls (Y: 130-250)
- Stable Audio Server URL
- Stable Prompt text area

### Bottom Section (Y: 555-775): Output & Status

#### Output Options (Left, Y: 555-690)
- Destination Mode selection
- Arrangement insertion controls
- New track creation buttons

#### Takes History (Right, Y: 555-715)
- Takes history dropdown
- Take name input
- Color index selection
- Apply button

#### Status Display (Full Width, Y: 700-775)
- Status messages
- Progress bar
- Error messages

#### Waveform Display (Far Right, Y: 700-820)
- Visual waveform display of processed audio

## Key Design Features

1. **Colored Stem Panels**: Each stem type has its own colored background panel for easy visual identification
   - Main Vocals: Red/Pink (#CC4C4C)
   - Backup Vocals: Blue (#8099E6)
   - Instrumental: Green (#66CC80)

2. **Prominent Pitch Control**: The pitch/octave control is large and prominently placed at the top right, matching the BS-3 style where octave control is emphasized

3. **Logical Grouping**: Controls are grouped by function:
   - Stem controls on the left
   - Main processing controls on the right
   - Advanced options in far right column
   - Status and output at the bottom

4. **Clean Visual Hierarchy**: Important controls (Process button, Pitch control) are larger and more prominent

5. **Consistent Spacing**: All controls have consistent spacing and alignment within their respective sections

## Window Dimensions

- Width: 1200px
- Height: 850px
- Provides ample space for all controls without crowding
