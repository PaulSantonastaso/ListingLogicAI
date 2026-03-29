from pydantic import BaseModel, Field
from typing import List, Optional


class VideoShot(BaseModel):
    order: int = Field(
        description="Shot order in the sequence, starting at 1"
    )
    image_filename: Optional[str] = Field(
        default=None,
        description="Filename of the property image to use for this shot. None if no images were uploaded."
    )
    room_type: Optional[str] = Field(
        default=None,
        description="Room or scene type shown in this shot such as kitchen, front_exterior, or living_room"
    )
    visible_features: List[str] = Field(
        default_factory=list,
        description="Key features visible in this shot that should be highlighted"
    )
    direction: str = Field(
        description="Brief shot direction for the agent. What to point the camera at, how to move, what to highlight. Written as a direct instruction."
    )


class VideoScript(BaseModel):
    platform: str = Field(
        description="Target platform: Instagram Reel, TikTok, or YouTube Short"
    )
    duration_seconds: int = Field(
        description="Target duration in seconds for this platform"
    )
    hook: str = Field(
        description="The opening line spoken or shown in the first 2-3 seconds. Must stop the scroll immediately."
    )
    shots: List[VideoShot] = Field(
        default_factory=list,
        description="Ordered list of shots that make up the video. Each shot maps to a property image or a described scene."
    )
    voiceover: str = Field(
        description="Full voiceover script the agent reads while filming or in post. Matches the shot sequence."
    )
    cta: str = Field(
        description="Closing call to action spoken or shown at the end of the video. Singular and direct."
    )


class VideoScriptSuite(BaseModel):
    reel: VideoScript = Field(
        description="Instagram Reel script. 15-30 seconds, hook-first, 4-6 shots, high energy."
    )
    tiktok: VideoScript = Field(
        description="TikTok script. 30-60 seconds, story-driven narrative, 6-8 shots, conversational tone."
    )
    youtube_short: VideoScript = Field(
        description="YouTube Short script. 45-60 seconds, most detail, 8-10 shots, neighborhood and lifestyle angle."
    )