import speech_recognition as sr
from speech_utils import synthesize_speech
from command_manager import load_commands, save_commands
from action_performer import match_command, suggest_similar_commands, perform_action

def listen_and_respond():
    """Lắng nghe lệnh của người dùng và phản hồi thích hợp."""
    recognizer = sr.Recognizer()
    
    while True:
        commands = load_commands()
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Hệ thống đang lắng nghe...")
            
            try:
                audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Đang nhận diện...")
                text = recognizer.recognize_google(audio_data, language='vi-VN')
                print("Bạn đã nói: " + text)
                
                # Xử lý lệnh
                action = match_command(text, commands)
                
                if action:
                    perform_action(action)
                else:
                    # Đưa ra các lệnh gần đúng
                    suggestions = suggest_similar_commands(text, commands)
                    if suggestions:
                        suggestion_text = "Hoặc có thể bạn muốn: " + ", ".join(suggestions)
                        response = f"Lệnh không rõ ràng. {suggestion_text}"
                        synthesize_speech(response)
                        
                        # Cung cấp thông tin chi tiết cho các lựa chọn
                        detail_text = "Các lựa chọn của bạn là: "
                        for i, suggestion in enumerate(suggestions):
                            detail_text += f"Số {i + 1} cho lệnh '{suggestion}'. "
                        
                        # Yêu cầu người dùng chọn lệnh bằng số
                        while True:
                            synthesize_speech(f"{detail_text}Vui lòng chọn lệnh chính xác bằng cách nói số.")
                            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                            user_choice = recognizer.recognize_google(audio_data, language='vi-VN').lower()
                            
                            # Xử lý lựa chọn của người dùng
                            try:
                                user_choice = user_choice.replace('số ', '').replace(' ', '')
                                if user_choice.isdigit():
                                    choice_number = int(user_choice)
                                    if 1 <= choice_number <= len(suggestions):
                                        chosen_command = suggestions[choice_number - 1]
                                        # Cập nhật lệnh mới vào danh sách lệnh đồng nghĩa
                                        if chosen_command in commands:
                                            commands[chosen_command].append(text)
                                        else:
                                            commands[chosen_command] = [text]
                                        save_commands(commands)
                                        # Xác nhận lệnh mới đã được lưu
                                        synthesize_speech(f"Lệnh '{chosen_command}' đã được lưu.")
                                        # Đọc lại các lệnh từ file JSON
                                        commands = load_commands()
                                        # Kiểm tra lại lệnh mới
                                        action = match_command(text, commands)
                                        if action:
                                            perform_action(action)
                                        break
                                    else:
                                        synthesize_speech("Số không hợp lệ. Vui lòng thử lại.")
                                else:
                                    synthesize_speech("Vui lòng nói số hợp lệ.")
                            except ValueError:
                                synthesize_speech("Tôi không nghe rõ số bạn nói. Vui lòng thử lại.")
                        
                    else:
                        # Không có gợi ý, yêu cầu người dùng nhập lệnh mới
                        synthesize_speech("Lệnh không rõ ràng. Bạn có muốn lưu lệnh này không? Nói 'Có' hoặc 'OK' để lưu hoặc 'Không' để bỏ qua.")
                        while True:
                            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                            user_response = recognizer.recognize_google(audio_data, language='vi-VN').lower()
                            
                            if "có" in user_response or "ok" in user_response:
                                synthesize_speech("Vui lòng nói rõ lệnh bạn muốn lưu.")
                                audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                                new_command = recognizer.recognize_google(audio_data, language='vi-VN').lower()
                                # Lưu lệnh mới vào file JSON
                                if new_command in commands:
                                    commands[new_command].append(text)
                                else:
                                    commands[new_command] = [text]
                                save_commands(commands)
                                # Xác nhận lệnh mới đã được lưu
                                synthesize_speech(f"Lệnh '{new_command}' đã được lưu.")
                                # Đọc lại các lệnh từ file JSON
                                commands = load_commands()
                                # Kiểm tra lại lệnh mới
                                action = match_command(text, commands)
                                if action:
                                    perform_action(action)
                                else:
                                    synthesize_speech(f"Lệnh '{new_command}' không hợp lệ. Vui lòng kiểm tra lại.")
                                break
                            elif "không" in user_response or "no" in user_response:
                                synthesize_speech("Lệnh đã bị bỏ qua.")
                                break
                            else:
                                synthesize_speech("Tôi không hiểu bạn nói gì. Vui lòng thử lại.")
                
            except sr.UnknownValueError:
                print("Không thể hiểu âm thanh.")
                synthesize_speech("Xin lỗi, tôi không thể hiểu bạn.")
            except sr.WaitTimeoutError:
                continue
            except sr.RequestError as e:
                print(f"Lỗi kết nối với dịch vụ nhận diện giọng nói: {e}")
                synthesize_speech("Xin lỗi, có lỗi với dịch vụ nhận diện giọng nói.")
                break

def main():
    """Hàm chính để bắt đầu quá trình lắng nghe và phản hồi."""
    listen_and_respond()

if __name__ == "__main__":
    main()
