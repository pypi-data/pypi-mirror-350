# coding: utf-8

from .data import Frame


class StreamParser:

    def __init__(self):
        self.buffer = b''

    def parse(self, data: bytes):
        """
        Parses the incoming data and returns a list of complete frames.

        Args:
            data (bytes): Incoming data as bytes.

        Returns:
            list[Frame]: A list of complete frames.
        """
        frames: list[Frame] = []

        # Add incoming data to the buffer
        self.buffer += data

        # Process buffer to extract complete frames
        while len(self.buffer) >= 54:
            # Extract one frame (54 bytes)
            frame = self.buffer[:54]
            frame_bytes = bytes(frame)
            frames.append(Frame.parse(frame_bytes))

            # Remove the frame from the buffer
            self.buffer = self.buffer[54:]

        # Return the list of complete frames
        return frames


# Example usage
if __name__ == "__main__":
    parser = StreamParser()

    # Simulate receiving fragmented data
    data_part1 = bytes([0x57, 0x54] + [0x00] * 52)  # First part of the frame
    data_part2 = bytes([0x57, 0x54] + [0x01] * 52)  # Second frame begins

    # Parse first part
    frames = parser.parse(data_part1)
    print("Frames after first part:", frames)  # Expect []

    # Parse second part
    frames = parser.parse(data_part2)
    print("Frames after second part:", frames)  # Expect two frames
