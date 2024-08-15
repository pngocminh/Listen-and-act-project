from speech_utils import synthesize_speech

def match_command(text, commands):
    """So sánh văn bản nhận được với các lệnh và từ đồng nghĩa để tìm lệnh phù hợp."""
    text = text.lower()
    scores = {}
    for action, phrases in commands.items():
        for phrase in phrases:
            if phrase in text:
                scores[action] = scores.get(action, 0) + 1
    return max(scores, key=scores.get, default=None) if scores else None

def suggest_similar_commands(text, commands):
    """Gợi ý các lệnh gần đúng dựa trên văn bản nhận được."""
    suggestions = []
    for action, phrases in commands.items():
        for phrase in phrases:
            if phrase in text:
                suggestions.append(action)
                break
    return suggestions

def perform_action(action):
    """Thực hiện hành động dựa trên lệnh được nhận diện."""
    if action == "bật đèn":
        synthesize_speech("Đang bật đèn.", speed=1.0)
    elif action == "tắt đèn":
        synthesize_speech("Đang tắt đèn.", speed=1.0)
    else:
        synthesize_speech("Lệnh không hợp lệ.", speed=1.0)
