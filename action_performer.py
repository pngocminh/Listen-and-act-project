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

def turn_on_light():
    synthesize_speech("Đang bật đèn." )

def turn_off_light():
    synthesize_speech("Đang tắt đèn." )

def handle_invalid_action():
    synthesize_speech("Lệnh không hợp lệ." )

def perform_action(action):
    # Tạo dictionary ánh xạ các hành động đến các hàm xử lý tương ứng
    actions = {
        "bật đèn": turn_on_light,
        "tắt đèn": turn_off_light
    }
    
    # Lấy hàm xử lý tương ứng, nếu không tìm thấy thì dùng handle_invalid_action
    action_func = actions.get(action, handle_invalid_action)
    
    # Thực thi hàm
    action_func()