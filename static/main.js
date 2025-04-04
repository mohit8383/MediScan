document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle.querySelector('i');
    const body = document.body;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.className = savedTheme;
        updateThemeIcon(savedTheme);
    }
    
    themeToggle.addEventListener('click', function() {
        if (body.classList.contains('light-theme')) {
            body.classList.replace('light-theme', 'dark-theme');
            localStorage.setItem('theme', 'dark-theme');
        } else {
            body.classList.replace('dark-theme', 'light-theme');
            localStorage.setItem('theme', 'light-theme');
        }
        updateThemeIcon(body.className);
    });
    
    function updateThemeIcon(theme) {
        if (theme === 'dark-theme') {
            themeIcon.className = 'fas fa-sun';
        } else {
            themeIcon.className = 'fas fa-moon';
        }
    }
    
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('nav ul');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('show');
        });
    }
    
    // Handle file upload UI
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.querySelector('.preview-container');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loaderContainer = document.getElementById('loaderContainer');
    const resultContainer = document.querySelector('.analysis-result');
    
    if (uploadArea && fileInput) {
        // Click on upload area triggers file input
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        // Handle drag and drop
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.classList.add('active');
        });
        
        uploadArea.addEventListener('dragleave', function() {
            uploadArea.classList.remove('active');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('active');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFiles(e.dataTransfer.files);
            }
        });
        
        // Handle file selection
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length) {
                handleFiles(fileInput.files);
            }
        });
    }
    
    // Function to handle file uploads and previews
    function handleFiles(files) {
        previewContainer.innerHTML = '';
        
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            
            if (file.type.startsWith('image/')) {
                const previewItem = document.createElement('div');
                previewItem.className = 'preview-item';
                
                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                
                const removeBtn = document.createElement('button');
                removeBtn.className = 'remove-btn';
                removeBtn.innerHTML = '<i class="fas fa-times"></i>';
                removeBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    previewItem.remove();
                    
                    // Create a new FileList without this file
                    const dt = new DataTransfer();
                    for (let j = 0; j < fileInput.files.length; j++) {
                        if (j !== i) {
                            dt.items.add(fileInput.files[j]);
                        }
                    }
                    fileInput.files = dt.files;
                });
                
                previewItem.appendChild(img);
                previewItem.appendChild(removeBtn);
                previewContainer.appendChild(previewItem);
            }
        }
        
        // Enable analyze button if files are uploaded
        analyzeBtn.disabled = previewContainer.children.length === 0;
    }
    
    // Global variable for audioBlob so that it's available during form submission
    let audioBlob = null;
    let mediaRecorder;
    let audioChunks = [];
    
    // Voice recording functionality
    const recordBtn = document.getElementById('recordBtn');
    const audioControls = document.querySelector('.audio-controls');
    const audioPlayer = document.querySelector('.audio-controls audio');
    
    if (recordBtn) {
        recordBtn.addEventListener('click', function() {
            if (recordBtn.textContent.includes('Start')) {
                startRecording();
            } else {
                stopRecording();
            }
        });
    }
    
    function startRecording() {
        audioChunks = [];
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });
                
                mediaRecorder.addEventListener('stop', () => {
                    // Assign to global audioBlob variable
                    audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    audioPlayer.src = audioUrl;
                    audioControls.style.display = 'block';
                    audioPlayer.style.display = 'block';
                    
                    // Optionally, you can upload audioBlob here if needed
                });
                
                mediaRecorder.start();
                recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
                recordBtn.classList.add('recording');
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                alert('Error accessing microphone. Please ensure you have given permission.');
            });
    }
    
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
            recordBtn.classList.remove('recording');
            
            // Stop all audio tracks
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
    
    // Form submission and analysis
    const analysisForm = document.getElementById('analysisForm');
    
    if (analysisForm) {
        analysisForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (fileInput.files.length === 0) {
                alert('Please upload at least one image for analysis.');
                return;
            }
            
            // Show loader
            loaderContainer.style.display = 'flex';
            
            // Create FormData object
            const formData = new FormData();
            
            // Append each selected file (if multiple files are allowed)
            for (let i = 0; i < fileInput.files.length; i++) {
                formData.append('files', fileInput.files[i]);
            }
            
            // Append audio if available
            if (audioBlob) {
                formData.append('audio', audioBlob, 'recording.webm');
            }
            
            // Append a primary image (using the first file)
            formData.append('image', fileInput.files[0]);
            
            // Append additional form data
            const patientName = document.getElementById('patientName');
            const patientAge = document.getElementById('patientAge');
            const symptoms = document.getElementById('symptoms');
            
            if (patientName) formData.append('patientName', patientName.value);
            if (patientAge) formData.append('patientAge', patientAge.value);
            if (symptoms) formData.append('symptoms', symptoms.value);
            
            // Send data to Flask backend
            fetch('/process_inputs', {
                method: 'POST',
                body: formData
            })              
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Hide loader
                loaderContainer.style.display = 'none';
                
                // Display results
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                // Hide loader
                loaderContainer.style.display = 'none';
                
                // Show error message
                alert('An error occurred during analysis. Please try again.');
            });
        });
    }
    
    // Display analysis results
    function displayResults(data) {
        // Show results container
        resultContainer.style.display = 'block';
        
        // Scroll to results
        resultContainer.scrollIntoView({ behavior: 'smooth' });
        
        // Update results content (customize based on your API response)
        const resultDetails = document.querySelector('.result-details');
        resultDetails.innerHTML = '';
        
        // Example: Display diagnosis if available
        if (data.diagnosis) {
            const diagnosisItem = document.createElement('div');
            diagnosisItem.className = 'result-item';
            
            const confidenceLevel = data.confidence || 0;
            const confidenceClass = confidenceLevel > 80 ? 'high' : confidenceLevel > 50 ? 'medium' : 'low';
            
            diagnosisItem.innerHTML = `
                <h4><i class="fas fa-stethoscope"></i> Diagnosis</h4>
                <p>${data.diagnosis}</p>
                <div class="confidence-bar">
                    <div class="confidence-level ${confidenceClass}" style="width: ${confidenceLevel}%"></div>
                </div>
                <p><small>Confidence: ${confidenceLevel}%</small></p>
            `;
            
            resultDetails.appendChild(diagnosisItem);
        }
        
        // Example: Display recommendations if available
        if (data.recommendations) {
            const recommendationsItem = document.createElement('div');
            recommendationsItem.className = 'result-item';
            
            let recommendationsHTML = '<h4><i class="fas fa-clipboard-list"></i> Recommendations</h4>';
            
            if (Array.isArray(data.recommendations)) {
                recommendationsHTML += '<ul>';
                data.recommendations.forEach(rec => {
                    recommendationsHTML += `<li>${rec}</li>`;
                });
                recommendationsHTML += '</ul>';
            } else {
                recommendationsHTML += `<p>${data.recommendations}</p>`;
            }
            
            recommendationsItem.innerHTML = recommendationsHTML;
            resultDetails.appendChild(recommendationsItem);
        }
        
        // Add more result items as needed
        
        // Add download report button functionality (if applicable)
        const downloadBtn = document.getElementById('downloadReport');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', function() {
                generatePDF(data);
            });
        }
    }
    
    // Generate and download PDF report (placeholder function)
    function generatePDF(data) {
        alert('PDF report generation would happen here in a production app.');
    }
    
    // Hide loader when page is fully loaded
    window.addEventListener('load', function() {
        loaderContainer.style.display = 'none';
    });
    
    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.step, .feature, .testimonial');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.classList.add('fade-in');
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on page load
});
