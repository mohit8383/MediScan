import os
import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# Core function remains the same
def process_inputs(audio_filepath, image_filepath):
    try:
        output_file = "final.mp3"
        
        speech_text = transcribe_with_groq(
            GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        ) if audio_filepath else "No audio input detected"

        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_text,
                encoded_image=encode_image(image_filepath),
                model="llama-3.2-11b-vision-preview"
            )
        else:
            doctor_response = "Please provide a medical image for analysis"

        if os.getenv("ELEVENLABS_API_KEY"):
            text_to_speech_with_elevenlabs(
                input_text=doctor_response,
                output_filepath=output_file
            )
        
        return speech_text, doctor_response, output_file
    except Exception as e:
        return f"Error: {str(e)}", "System Error", ""

# Fresh, minimalist CSS
fresh_css = """
body {
    font-family: 'DM Sans', sans-serif;
    background-color: #FFFFFF;
}

/* Light, airy design */
.container {
    max-width: 1200px;
    margin: 0 auto;
}

/* Fresh, minimal header */
.header-minimal {
    padding: 1.5rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid #f0f0f0;
}

/* Clean cards with subtle shadows */
.fresh-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: all 0.2s ease;
    border: 1px solid #f0f0f0;
    overflow: hidden;
}

/* Simple, clear action buttons */
.action-button {
    background: #4CAF50 !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
}

/* Media inputs with subtle highlights */
.media-input {
    border: 2px dashed #E0E0E0 !important;
    border-radius: 8px !important;
    padding: 1.5rem !important;
}

.media-input:hover {
    border-color: #4CAF50 !important;
    background: rgba(76, 175, 80, 0.03) !important;
}

/* Results area with clean typography */
.result-area {
    line-height: 1.6 !important;
    padding: 1rem !important;
}

/* Simple tabs with clean borders */
.tab-container {
    border-bottom: 1px solid #f0f0f0 !important;
}

.tab-item {
    padding: 0.75rem 1rem !important;
    margin-right: 1rem !important;
    border-bottom: 2px solid transparent !important;
}

.tab-item.active {
    border-bottom: 2px solid #4CAF50 !important;
    color: #4CAF50 !important;
}

/* Clean audio player */
audio {
    width: 100% !important;
    margin-top: 1rem !important;
    border-radius: 6px !important;
}
"""

# Your system prompt
system_prompt = """You have to act as a professional doctor..."""

# Fresh, simple UI
with gr.Blocks(css=fresh_css) as app:
    # Simple, clean header
    gr.HTML("""
    <div class="header-minimal">
        <h2 style="margin:0; color:#333; font-weight:500;">MediScan</h2>
        <p style="margin:0; color:#666; font-size:15px;">Simple medical image analysis</p>
    </div>
    """)
    
    with gr.Row(equal_height=True):
        # Left panel for inputs
        with gr.Column():
            gr.Markdown("#### Provide Information")
            
            # Simple voice input
            with gr.Group(elem_classes="fresh-card"):
                audio_input = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="Describe symptoms",
                    elem_classes="media-input"
                )
            
            # Simple image upload
            with gr.Group(elem_classes="fresh-card"):
                image_input = gr.Image(
                    type="filepath",
                    label="Upload medical image",
                    elem_classes="media-input"
                )
            
            # Clean action button
            submit_btn = gr.Button("Analyze", elem_classes="action-button")

        # Right panel for outputs
        with gr.Column():
            gr.Markdown("#### Analysis Results")
            
            with gr.Group(elem_classes="fresh-card"):
                transcription_output = gr.Textbox(
                    label="Your description",
                    elem_classes="result-area"
                )
                
                diagnosis_output = gr.Textbox(
                    label="Medical findings",
                    elem_classes="result-area"
                )
                
                audio_output = gr.Audio(
                    label="Voice explanation",
                    autoplay=True
                )
    
    # Simple footer
    gr.HTML("""
    <div style="text-align:center; margin-top:2rem; color:#888; font-size:12px;">
        For educational purposes only • Not a substitute for professional medical advice
    </div>
    """)
    
    # Event handling
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[transcription_output, diagnosis_output, audio_output]
    )

# Launch the application
app.launch(debug=False)