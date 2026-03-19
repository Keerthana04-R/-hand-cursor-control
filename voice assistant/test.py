import speech_recognition as sr
r = sr.Recognizer()
r.energy_threshold = 50
r.dynamic_energy_threshold = False

with sr.Microphone(device_index=11) as source:
    print("Adjusting for noise...")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Speak now!")
    try:
        audio = r.listen(source, timeout=8, phrase_time_limit=8)
        print("Got audio, size:", len(audio.get_raw_data()), "bytes")
        print("Result:", r.recognize_google(audio, language="en-IN"))
    except sr.WaitTimeoutError:
        print("❌ Timeout - mic not picking up voice")
    except sr.UnknownValueError:
        print("❓ Heard audio but could not understand")
    except Exception as e:
        print("Error:", e)