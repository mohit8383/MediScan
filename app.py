import os
import tempfile
from flask import Flask, request, jsonify, send_file, render_template
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

app = Flask(__name__)

# Your system prompt
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). And dont to text bold as when speaking, it says asterisk too. Ans speak in same language, in which u get user input, if no user input, u can do in english. No preamble, start your answer right away please"""

@app.route('/')
def index():
    # Serve the HTML page
    return render_template('index.html')

@app.route('/process_inputs', methods=['POST'])
def process_inputs():
    try:
        # Create temp files for processing
        audio_file = None
        image_file = None
        
        # Handle audio file upload
        if 'audio' in request.files:
            audio = request.files['audio']
            audio_fd, audio_filepath = tempfile.mkstemp(suffix='.webm')
            audio.save(audio_filepath)
            os.close(audio_fd)
            audio_file = audio_filepath
        
        # Handle image file upload
        if 'image' in request.files:
            image = request.files['image']
            image_fd, image_filepath = tempfile.mkstemp(suffix='.jpg')
            image.save(image_filepath)
            os.close(image_fd)
            image_file = image_filepath
        
        # Process the inputs
        speech_text = "No audio input detected"
        doctor_response = "Please provide a medical image for analysis"
        audio_url = None
        
        # Transcribe audio if available
        if audio_file:
            speech_text = transcribe_with_groq(
                GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
                audio_filepath=audio_file,
                stt_model="whisper-large-v3"
            )
        
        # Analyze image if available
        if image_file:
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_text,
                encoded_image=encode_image(image_file),
                model="llama-3.2-11b-vision-preview"
            )
        
        # Generate audio response if API key available
        output_file = None
        if os.getenv("ELEVENLABS_API_KEY"):
            output_fd, output_filepath = tempfile.mkstemp(suffix='.mp3')
            os.close(output_fd)
            text_to_speech_with_elevenlabs(
                input_text=doctor_response,
                output_filepath=output_filepath
            )
            output_file = output_filepath
        
        # Clean up temporary files
        if audio_file:
            os.unlink(audio_file)
        if image_file:
            os.unlink(image_file)
        
        # Prepare response
        response = {
            'transcription': speech_text,
            'diagnosis': doctor_response
        }
        
        # If audio was generated, return its URL
        if output_file:
            response['audio_url'] = f'/audio/{os.path.basename(output_file)}'
            # Store output file path to serve later
            app.config[os.path.basename(output_file)] = output_file
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    # Get the file path from app config
    file_path = app.config.get(filename)
    if not file_path:
        return "File not found", 404
    
    # Serve the audio file
    return send_file(file_path, mimetype='audio/mp3')

if __name__ == '__main__':
    # Make sure the app.config can store temp files
    app.config.update(SEND_FILE_MAX_AGE_DEFAULT=0)
    
    # Run the Flask app
    import os
import tempfile
from flask import Flask, request, jsonify, send_file, render_template
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

app = Flask(__name__)

# Your system prompt
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

@app.route('/')
def index():
    # Serve the HTML page
    return render_template('index.html')

@app.route('/process_inputs', methods=['POST'])
def process_inputs():
    try:
        # Create temp files for processing
        audio_file = None
        image_file = None
        
        # Handle audio file upload
        if 'audio' in request.files:
            audio = request.files['audio']
            audio_fd, audio_filepath = tempfile.mkstemp(suffix='.webm')
            audio.save(audio_filepath)
            os.close(audio_fd)
            audio_file = audio_filepath
        
        # Handle image file upload
        if 'image' in request.files:
            image = request.files['image']
            image_fd, image_filepath = tempfile.mkstemp(suffix='.jpg')
            image.save(image_filepath)
            os.close(image_fd)
            image_file = image_filepath
        
        # Process the inputs
        speech_text = "No audio input detected"
        doctor_response = "Please provide a medical image for analysis"
        audio_url = None
        
        # Transcribe audio if available
        if audio_file:
            speech_text = transcribe_with_groq(
                GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
                audio_filepath=audio_file,
                stt_model="whisper-large-v3"
            )
        
        # Analyze image if available
        if image_file:
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_text,
                encoded_image=encode_image(image_file),
                model="llama-3.2-11b-vision-preview"
            )
        
        # Generate audio response if API key available
        output_file = None
        if os.getenv("ELEVENLABS_API_KEY"):
            output_fd, output_filepath = tempfile.mkstemp(suffix='.mp3')
            os.close(output_fd)
            text_to_speech_with_elevenlabs(
                input_text=doctor_response,
                output_filepath=output_filepath
            )
            output_file = output_filepath
        
        # Clean up temporary files
        if audio_file:
            os.unlink(audio_file)
        if image_file:
            os.unlink(image_file)
        
        # Prepare response
        response = {
            'transcription': speech_text,
            'diagnosis': doctor_response
        }
        
        # If audio was generated, return its URL
        if output_file:
            response['audio_url'] = f'/audio/{os.path.basename(output_file)}'
            # Store output file path to serve later
            app.config[os.path.basename(output_file)] = output_file
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    # Get the file path from app config
    file_path = app.config.get(filename)
    if not file_path:
        return "File not found", 404
    
    # Serve the audio file
    return send_file(file_path, mimetype='audio/mp3')

if __name__ == '__main__':
    # Make sure the app.config can store temp files
    app.config.update(SEND_FILE_MAX_AGE_DEFAULT=0)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
