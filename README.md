# Quick Image Sequence Process

A ComfyUI plugin for quick image sequence processing. This plugin allows users to manipulate frame sequences with various operations including frame insertion, deletion, and duplication.

## Features

1. **Frame Insertion Between Frames**:
   - Set the number of frames to insert between existing frames
   - Choose whether to copy from the previous or next frame
   - Example: With frames_between=2, sequence [A,B] becomes [A,A,A,B] or [A,B,B,B]

2. **Quick Process First Frames**:
   - Add or remove frames at the beginning of the sequence
   - Positive values: Add duplicates of the first frame
   - Negative values: Remove frames from the beginning
   - Example: With quick_process_first_frames=2, [A,B,C] becomes [A,A,A,B,C]
   - Example: With quick_process_first_frames=-1, [A,B,C] becomes [B,C]

3. **Quick Process Last Frames**:
   - Add or remove frames at the end of the sequence
   - Positive values: Add duplicates of the last frame
   - Negative values: Remove frames from the end
   - Example: With quick_process_last_frames=2, [A,B,C] becomes [A,B,C,C,C]
   - Example: With quick_process_last_frames=-1, [A,B,C] becomes [A,B]

4. **Processing Order Control**:
   - Choose whether to process first/last frames before or after the between-frame operations
   - Affects the final result when combining multiple operations
   - "Yes": Process first/last frames first
   - "No": Process between-frames first

5. **Real-time Frame Count Display**:
   - Shows the total number of frames after processing
   - Helps track sequence length changes

## Installation

1. Clone this repository into your ComfyUI's `custom_nodes` directory:
   ```bash
   cd custom_nodes
   git clone https://github.com/yourusername/ComfyUI-QuickImageSequenceProcess.git
   ```
2. Restart ComfyUI
3. Find "Quick Image Sequence Process" in the node menu

## Usage Example

1. Load an image sequence into ComfyUI
2. Add the "Quick Image Sequence Process" node
3. Configure parameters:
   - `frames_between`: Number of frames to insert between existing frames
   - `copy_frame`: Choose "previous" or "next" for inserted frames
   - `quick_process_first_frames`: Add/remove frames at start (negative to remove)
   - `quick_process_last_frames`: Add/remove frames at end (negative to remove)
   - `process_F_L_frames_first`: Choose processing order priority

## Output

The node outputs:
- `image`: The processed image sequence
- `width`: Frame width
- `height`: Frame height
- `count`: Total number of frames in the sequence

## License

Copyright 2024 junnpaku_11

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

