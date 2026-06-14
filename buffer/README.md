# Buffer Scheduler Skill

Schedule social media captions for an AI For You post to Buffer in one command.

Invoke with `/buffer [post_number]` or `/buffer [post_number] [scheduled_at]`.

Reads the Instagram/TikTok, LinkedIn, Twitter, and Threads content files for the given post, extracts the platform captions, and schedules them via the Buffer MCP (two accounts: `insta-buffer` for Instagram/LinkedIn/Twitter, `threads-buffer` for Threads). Registers each queued post in the asset DB.
