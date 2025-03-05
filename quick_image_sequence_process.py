"""
@author: kazeyori
@title: Quick Image Sequence Process
@nickname: QuickSeq
@description: A ComfyUI plugin for efficient image sequence processing. Features frame insertion, duplication, and removal with intuitive controls.
"""

# quick_image_sequence_process.py
import numpy as np
import torch

class QuickImageSequenceProcessNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  # Input image sequence
                "frames_between": ("INT", {"default": 1}),  # Number of frames to copy between each frame
                "copy_frame": (["previous", "next"],),  # Whether to copy the previous or next frame
                "fill_mode": (["copy_frame", "white", "black"],),  # Fill mode for added frames
                "quick_process_first_frames": ("INT", {"default": 0}),  # Number of frames to add/remove at the beginning (negative values for removal)
                "quick_process_last_frames": ("INT", {"default": 0}),  # Number of frames to add/remove at the end (negative values for removal)
                "process_F_L_frames_first": (["yes", "no"],),  # Whether to prioritize processing first and last frames
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT")  # Output: image, width, height, count
    RETURN_NAMES = ("image", "width", "height", "count")
    FUNCTION = "edit_image_sequence"

    CATEGORY = "image/sequence"

    def create_solid_frame(self, reference_frame, color="white"):
        """Create a solid white or black frame with the same dimensions as the reference frame"""
        # Get dimensions from reference frame
        if isinstance(reference_frame, torch.Tensor):
            h, w = reference_frame.shape[0], reference_frame.shape[1]
            c = reference_frame.shape[2] if len(reference_frame.shape) > 2 else 3
            
            # Create solid frame
            if color == "white":
                solid_frame = torch.ones((h, w, c), dtype=reference_frame.dtype)
            else:  # black
                solid_frame = torch.zeros((h, w, c), dtype=reference_frame.dtype)
                
            return solid_frame
        else:
            raise TypeError("Reference frame must be a torch tensor")

    def process_between_frames(self, images, frames_between, copy_frame, fill_mode):
        """Process middle frames (including frame insertion)"""
        new_images = []
        for i in range(len(images)):
            # Add current frame
            new_images.append(images[i])

            # If not the last frame, insert frames between current and next
            if i < len(images) - 1:
                if fill_mode == "copy_frame":
                    # Use original copy frame logic
                    if copy_frame == "previous":
                        frame_to_add = images[i]
                    else:  # "next"
                        frame_to_add = images[i + 1]
                elif fill_mode == "white":
                    frame_to_add = self.create_solid_frame(images[i], "white")
                else:  # "black"
                    frame_to_add = self.create_solid_frame(images[i], "black")

                for _ in range(frames_between):
                    new_images.append(frame_to_add)
        return new_images

    def process_end_frames(self, images, quick_process_first_frames, quick_process_last_frames, fill_mode):
        """Process first and last frames (adding or removing)"""
        new_images = list(images)  # Convert to list for modification

        if quick_process_first_frames >= 0:
            # Add frames at the beginning
            if fill_mode == "copy_frame":
                first_frame = new_images[0]
                frames_to_add = [first_frame] * quick_process_first_frames
            elif fill_mode == "white":
                first_frame = self.create_solid_frame(new_images[0], "white")
                frames_to_add = [first_frame] * quick_process_first_frames
            else:  # "black"
                first_frame = self.create_solid_frame(new_images[0], "black")
                frames_to_add = [first_frame] * quick_process_first_frames
            
            new_images = frames_to_add + new_images
        else:
            # Remove frames from the beginning
            new_images = new_images[-quick_process_first_frames:]

        if quick_process_last_frames >= 0:
            # Add frames at the end
            if fill_mode == "copy_frame":
                last_frame = new_images[-1]
                frames_to_add = [last_frame] * quick_process_last_frames
            elif fill_mode == "white":
                last_frame = self.create_solid_frame(new_images[-1], "white")
                frames_to_add = [last_frame] * quick_process_last_frames
            else:  # "black"
                last_frame = self.create_solid_frame(new_images[-1], "black")
                frames_to_add = [last_frame] * quick_process_last_frames
            
            new_images.extend(frames_to_add)
        else:
            # Remove frames from the end
            new_images = new_images[:quick_process_last_frames]

        return new_images

    def edit_image_sequence(self, images, frames_between, copy_frame, fill_mode, quick_process_first_frames, quick_process_last_frames, process_F_L_frames_first):
        """
        Edit image sequence:
        1. Process order determined by process_F_L_frames_first
        2. Insert specified number of frames between frames (copied or solid color)
        3. Add or remove frames at the beginning and end
        """
        # Ensure input is PyTorch tensor
        if isinstance(images, np.ndarray):
            images = torch.from_numpy(images)

        if process_F_L_frames_first == "yes":
            # Process first/last frames first, then middle frames
            intermediate_images = self.process_end_frames(images, quick_process_first_frames, quick_process_last_frames, fill_mode)
            new_images = self.process_between_frames(intermediate_images, frames_between, copy_frame, fill_mode)
        else:
            # Process middle frames first, then first/last frames
            intermediate_images = self.process_between_frames(images, frames_between, copy_frame, fill_mode)
            new_images = self.process_end_frames(intermediate_images, quick_process_first_frames, quick_process_last_frames, fill_mode)

        # Ensure at least one frame remains
        if not new_images:
            raise ValueError("No frames remaining after processing. Please adjust parameters to ensure at least one frame.")

        # Convert image sequence to PyTorch tensor
        new_images = torch.stack(new_images)

        # Get dimensions
        width = new_images.shape[2]
        height = new_images.shape[1]
        frame_count = len(new_images)

        # Display frame count
        print(f"Processed sequence contains {frame_count} frames")

        # Return results
        return (new_images, width, height, frame_count)