document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('file');
    const statusDiv = document.getElementById('status');

    from flask_cors import CORS
    app = Flask(__name__)
    CORS(app)


    if (!fileInput.files.length) {
        statusDiv.textContent = "Please select a file to upload.";
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    statusDiv.textContent = "Uploading and processing...";

    try {
        const response = await fetch('https://your-app-name.onrender.com/upload', { // Replace with your Render URL
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'output.txt';
            document.body.appendChild(a);
            a.click();
            a.remove();
            statusDiv.textContent = "File processed. Download started.";
        } else {
            const errorData = await response.json();
            statusDiv.textContent = `Error: ${errorData.error || "Unknown error"}`;
        }
    } catch (error) {
        console.error(error);
        statusDiv.textContent = "An error occurred during upload.";
    }
});
