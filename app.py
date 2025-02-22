import streamlit as st
import base64
import os

def get_html_file():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#4CAF50">
    <title>NFC Tracker</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        h1, h2, h3 {
            color: #333;
        }
        .tag-status {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .status-indicator {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .connected {
            background-color: #4CAF50;
        }
        .disconnected {
            background-color: #F44336;
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .history-entry {
            border-left: 3px solid #2196F3;
            padding-left: 15px;
            margin-bottom: 15px;
        }
        .timestamp {
            color: #666;
            font-size: 14px;
        }
        .changes {
            margin: 5px 0;
        }
        .user {
            font-style: italic;
            color: #555;
        }
        @media (max-width: 600px) {
            .container {
                padding: 10px;
            }
            .card {
                padding: 15px;
            }
        }
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .action-buttons button {
            flex: 1;
        }
        #notification {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            padding: 10px 20px;
            background-color: #333;
            color: white;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            display: none;
        }
    </style>
    <!-- Add manifest for PWA support -->
    <link rel="manifest" href="data:application/manifest+json,{
        &quot;name&quot;: &quot;NFC Tracker&quot;,
        &quot;short_name&quot;: &quot;NFCTrack&quot;,
        &quot;start_url&quot;: &quot;.&quot;,
        &quot;display&quot;: &quot;standalone&quot;,
        &quot;background_color&quot;: &quot;#ffffff&quot;,
        &quot;theme_color&quot;: &quot;#4CAF50&quot;,
        &quot;description&quot;: &quot;App for tracking items with NFC tags&quot;,
        &quot;icons&quot;: [{
            &quot;src&quot;: &quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALQAAAC0CAMAAAAKE/YAAAAAeFBMVEUAAABGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEZGrEYFzeThAAAAJ3RSTlMAIEBQcICPv9/P7yAwMEAgMFBgUEBwgJC/3+/f36CQoIBwsLCgYNFTaInrAAAC0klEQVR4Ae3dvbKbMBCGYe2SrE7p08vZl9jJ3P81pmGKZGwsSLD83ecGnhkQkhEQoR07duzYsWPHjh0pS5eV2FUuW9LTV8/gjr9Oru8J3mT8EGfCh5T2jItVKc1Hwk8JfyqFt4S14JwZw0KYcSwzIsXYEzbBGKlwtgo72RX+SOYKl2SrhgvZnB3+wtn7cPzLn0rGvn6ZkozPOV++4is+jjxLOK/xTWz51iy8wneJY8uzaVzheyNcZIHvhXCR8RDfibMkuSQgdnUhQ3LqCDHEFE8R4rpIEUNGiP3FBdLAGDFdYiEJnSNmP/IVp7XEiCUiXlRuPDzGDAL3dERMs4/gTCNifuPRkbhIMNT3L1eBu3V+J/CQtgjuBJ6lBwLF2VM5UNd3l6vA3Tr9c/BQTu4EHrK96P/kKnC35gQecspJXIFHkruUw+XiKnC3zqSWw+U6kAXudiDwnEgth8u14CpwfWxJ4LkK5XC5+MfP/TqRBA51+0kuh8vlvUhw6xXJPQklcLnuD65yP9z92KXLvWRY7l/uKfZa7tqQ/kPo5S4S0n+TLtcKPy4t14p+XlquX1mPy7Vi3qeW6z29PC/Xc6MXl+u91/O4XKtJjQGXa/UKdLlWw0aXa7W+9rlcq4m0y7UauctFrntTcvUabnP1Km9z9XoAc/V6KHT1ejB29Xo5d/VagHD1WiJx9eAFT/7x91os2i8WbO0X7CsLdtabLEY0mqzaNFat2rVaNmu3b9du32zfrt3uYcsj1JZHqC3PsBueobc8xG95it/wGH/Lc/yGDxI0fJKh4aMUDZ/laPgwScOnWRo+TvPqaZ4JHlJNSMrV6+GQyHzkmNzc8V2jdWxp+ERXQ1u7G/UWDxEaGpo8xTyTzdLIJCPbaZk0WR+0frJT6QZvavEuZcahCs4ztGnlcItbdYozfDJhR4g+nJ2d38gYXZ6P8Bn+ufgFhyJeUVlFWhsAAAAASUVORK5CYII=&quot;,
            &quot;sizes&quot;: &quot;192x192&quot;,
            &quot;type&quot;: &quot;image/png&quot;
        }]
    }">
</head>
<body>
    <div id="notification"></div>
    <div class="container">
        <h1>NFC Tracker</h1>
        
        <div class="card">
            <div class="tag-status">
                <div id="statusIndicator" class="status-indicator disconnected"></div>
                <div id="statusText">Checking NFC availability...</div>
            </div>
            
            <div class="action-buttons">
                <button id="readButton">Read NFC Tag</button>
                <button id="writeButton" disabled>Write to Tag</button>
            </div>
            
            <div id="tagContent" style="display: none;">
                <h2>Tag Information</h2>
                <div>
                    <label for="itemName">Item Name:</label>
                    <input type="text" id="itemName" placeholder="Enter item name">
                </div>
                
                <div>
                    <label for="description">Description:</label>
                    <textarea id="description" rows="4" placeholder="Enter description"></textarea>
                </div>
                
                <div>
                    <label for="changes">What changed:</label>
                    <input type="text" id="changes" placeholder="Describe your changes">
                </div>
                
                <div>
                    <label for="user">Your name:</label>
                    <input type="text" id="user" placeholder="Enter your name">
                </div>
                
                <div id="history">
                    <h3>History</h3>
                    <div id="historyEntries"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Register service worker for PWA support
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('data:text/javascript;base64,' + btoa(`
                self.addEventListener('install', (event) => {
                    self.skipWaiting();
                });
                self.addEventListener('fetch', (event) => {
                    event.respondWith(fetch(event.request));
                });
            `)).then(() => {
                console.log('Service worker registered');
            }).catch(err => {
                console.error('Service worker registration failed', err);
            });
        }

        // Global variables
        let tagData = null;
        let nfcEnabled = false;
        let ndefInstance = null;
        
        // Helper function to show notifications
        function showNotification(message, duration = 3000) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, duration);
        }

        // Check for NFC support using multiple methods
        function checkNfcSupport() {
            // Primary method: Web NFC API
            if ('NDEFReader' in window) {
                console.log("Web NFC is available");
                document.getElementById('statusText').textContent = 'NFC Available - Click Read Tag Button';
                nfcEnabled = true;
                return true;
            }
            
            // Fallback method: navigator.nfc (older API)
            if ('nfc' in navigator) {
                console.log("Using alternative NFC API");
                document.getElementById('statusText').textContent = 'Using alternative NFC API';
                nfcEnabled = true;
                return true;
            }

            // Try getWebNFC polyfill if available
            if (typeof(getWebNFC) !== 'undefined') {
                try {
                    const webNFC = getWebNFC();
                    if (webNFC) {
                        console.log("Using WebNFC polyfill");
                        window.NDEFReader = webNFC.NDEFReader;
                        nfcEnabled = true;
                        return true;
                    }
                } catch (e) {
                    console.error("Error with WebNFC polyfill:", e);
                }
            }
            
            // Add compatibility warning and debug info
            showNotification("NFC not supported. Please ensure: 1) Chrome v89+, 2) NFC enabled, 3) HTTPS or localhost", 10000);
            document.getElementById('statusText').textContent = 'NFC not supported or not accessible';
            
            const debugInfo = document.createElement('div');
            debugInfo.innerHTML = `
                <div style="margin-top: 20px; padding: 10px; background: #f8f8f8; border: 1px solid #ddd; border-radius: 5px;">
                    <h3>Troubleshooting Information</h3>
                    <p>Browser: ${navigator.userAgent}</p>
                    <p>Is Secure Context: ${window.isSecureContext ? 'Yes' : 'No (Web NFC requires HTTPS)'}</p>
                    <p>Protocol: ${window.location.protocol}</p>
                    <p>Origin: ${window.location.origin}</p>
                    <p>Please verify:</p>
                    <ul>
                        <li>You are using Chrome for Android (version 89+)</li>
                        <li>NFC is enabled in your phone settings</li>
                        <li>The page is loaded over HTTPS or from localhost</li>
                        <li>Your device has NFC hardware</li>
                    </ul>
                    <p>Alternative approach: <button id="intentButton">Use Android Intent</button></p>
                </div>
            `;
            document.querySelector('.card').appendChild(debugInfo);
            
            // Add intent fallback
            document.getElementById('intentButton').addEventListener('click', function() {
                // Try to launch NFC via intent
                const intentUrl = `intent://scan/#Intent;scheme=nfc;package=com.android.nfc;end`;
                window.location.href = intentUrl;
            });
            
            return false;
        }
        
        // Read NFC tag using Web NFC API
        async function readNfcTag() {
            if (!nfcEnabled) {
                showNotification("NFC is not supported on this device/browser");
                return;
            }
            
            try {
                document.getElementById('statusText').textContent = 'Waiting for NFC tag...';
                document.getElementById('statusIndicator').classList.remove('connected');
                document.getElementById('statusIndicator').classList.add('disconnected');
                
                if ('NDEFReader' in window) {
                    // Use standard Web NFC API
                    ndefInstance = new NDEFReader();
                    await ndefInstance.scan();
                    
                    showNotification("Scan started - tap an NFC tag");
                    
                    ndefInstance.addEventListener("reading", ({ message, serialNumber }) => {
                        console.log(`> Serial Number: ${serialNumber}`);
                        console.log(`> Records: (${message.records.length})`);
                        
                        processNfcReading(message);
                    });
                } else if ('nfc' in navigator) {
                    // Use older navigator.nfc API if available
                    navigator.nfc.watch({
                        mode: 'any',
                        callback: function(message) {
                            processNfcReading(message);
                        },
                        onerror: function(error) {
                            console.error("NFC error:", error);
                            showNotification("NFC error: " + error);
                        }
                    });
                }
            } catch (error) {
                console.error(`Error scanning: ${error.message}`);
                showNotification("Error: " + error.message);
                
                // Special handling for permission errors
                if (error.name === 'NotAllowedError') {
                    showNotification("NFC permission denied. Please enable NFC in your settings.", 5000);
                }
                
                // Special handling for security errors
                if (error.name === 'SecurityError') {
                    showNotification("Security error. Make sure you're using HTTPS or localhost.", 5000);
                }
            }
        }
        
        // Process NFC reading data
        function processNfcReading(message) {
            try {
                // Process the first record
                if (message.records && message.records.length > 0) {
                    const record = message.records[0];
                    
                    if (record.recordType === "text") {
                        const decoder = new TextDecoder();
                        let textData;
                        
                        // Handle different record data structures
                        if (record.data instanceof ArrayBuffer) {
                            textData = decoder.decode(record.data);
                        } else if (record.data && typeof record.data.buffer !== 'undefined') {
                            textData = decoder.decode(record.data.buffer);
                        } else if (typeof record.text === 'function') {
                            textData = record.text();
                        } else if (typeof record.text === 'string') {
                            textData = record.text;
                        }
                        
                        try {
                            tagData = JSON.parse(textData);
                            updateUIWithTagData(tagData);
                            document.getElementById('writeButton').disabled = false;
                            showNotification("Tag read successfully!");
                        } catch (e) {
                            // If not valid JSON, initialize a new data structure
                            tagData = {
                                "item_name": "",
                                "description": "",
                                "history": []
                            };
                            updateUIWithTagData(tagData);
                            document.getElementById('writeButton').disabled = false;
                            showNotification("New tag detected - ready to write");
                        }
                    }
                }
                
                // Update status indicator
                document.getElementById('statusIndicator').classList.remove('disconnected');
                document.getElementById('statusIndicator').classList.add('connected');
                document.getElementById('statusText').textContent = 'NFC Tag Connected';
                
            } catch (error) {
                console.error("Error processing tag data:", error);
                showNotification("Error reading tag: " + error.message);
            }
        }
        
        // Write to NFC tag
        async function writeNfcTag() {
            if (!nfcEnabled || !tagData) return;
            
            try {
                // Update tag data
                const itemName = document.getElementById('itemName').value;
                const description = document.getElementById('description').value;
                const changes = document.getElementById('changes').value;
                const user = document.getElementById('user').value;
                
                if (!changes) {
                    showNotification("Please describe what you changed");
                    return;
                }
                
                if (!user) {
                    showNotification("Please enter your name");
                    return;
                }
                
                // Create history entry with human-readable timestamp
                const now = new Date();
                const humanTimestamp = now.toLocaleString('en-US', { 
                    month: 'long', 
                    day: 'numeric', 
                    year: 'numeric',
                    hour: 'numeric',
                    minute: 'numeric',
                    hour12: true
                });
                
                const historyEntry = {
                    "timestamp": now.toISOString(),
                    "human_timestamp": humanTimestamp,
                    "changes": changes,
                    "user": user
                };
                
                // Update tag data structure
                const updatedData = {
                    "item_name": itemName,
                    "description": description,
                    "history": [...(tagData.history || []), historyEntry]
                };
                
                document.getElementById('statusText').textContent = 'Tap tag to write...';
                showNotification("Tap tag to write data");
                
                if ('NDEFReader' in window) {
                    // Use standard Web NFC API
                    const ndef = new NDEFReader();
                    await ndef.write({
                        records: [{
                            recordType: "text",
                            data: JSON.stringify(updatedData)
                        }]
                    });
                } else if ('nfc' in navigator) {
                    // Use older navigator.nfc API if available
                    await navigator.nfc.push({
                        records: [{
                            type: "text",
                            text: JSON.stringify(updatedData)
                        }]
                    });
                }
                
                // Update local data
                tagData = updatedData;
                updateUIWithTagData(tagData);
                
                // Clear change fields
                document.getElementById('changes').value = '';
                showNotification("Tag updated successfully!");
                
            } catch (error) {
                console.error(`Error writing: ${error.message}`);
                showNotification("Error writing to tag: " + error.message);
            }
        }
        
        // Update UI with tag data
        function updateUIWithTagData(data) {
            // Show tag content
            document.getElementById('tagContent').style.display = 'block';
            
            // Fill form fields
            document.getElementById('itemName').value = data.item_name || '';
            document.getElementById('description').value = data.description || '';
            
            // Update history
            const historyContainer = document.getElementById('historyEntries');
            historyContainer.innerHTML = '';
            
            if (data.history && data.history.length > 0) {
                data.history.slice().reverse().forEach(entry => {
                    const historyEntry = document.createElement('div');
                    historyEntry.className = 'history-entry';
                    
                    // Use human-readable timestamp if available, otherwise format the ISO timestamp
                    const displayTime = entry.human_timestamp || new Date(entry.timestamp).toLocaleString();
                    
                    historyEntry.innerHTML = `
                        <div class="timestamp">${displayTime}</div>
                        <div class="changes">${entry.changes}</div>
                        <div class="user">By: ${entry.user}</div>
                    `;
                    
                    historyContainer.appendChild(historyEntry);
                });
            } else {
                historyContainer.innerHTML = '<p>No history available</p>';
            }
        }
        
        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            // Check NFC support
            checkNfcSupport();
            
            // Add event listeners for buttons
            document.getElementById('readButton').addEventListener('click', readNfcTag);
            document.getElementById('writeButton').addEventListener('click', writeNfcTag);
        });
    </script>
</body>
</html>"""
    return html_content

def main():
    st.set_page_config(
        page_title="NFC Tag Tracker",
        page_icon="📱",
        layout="wide"
    )
    
    st.title("NFC Tag Tracker App")
    
    st.markdown("""
    ## Instructions
    
    1. Open this app on your Android phone with Chrome browser
    2. Click the link below to launch the NFC app in a new tab
    3. Use the app to read and write to NFC tags
    
    ### Requirements:
    
    - Android phone with NFC capability
    - Chrome browser (version 89+)
    - NFC enabled in your phone settings
    """)
    
    # Create HTML file for download
    html_content = get_html_file()
    
    # Create an inline HTML link that opens in a new tab
    html_data = html_content.encode("utf-8")
    b64_html = base64.b64encode(html_data).decode()
    
    # Create the HTML for the app page
    st.markdown(f'<a href="data:text/html;base64,{b64_html}" target="_blank" style="display: inline-block; padding: 12px 24px; margin: 15px 0; background-color: #4CAF50; color: white; text-decoration: none; font-weight: bold; border-radius: 4px; text-align: center;">Open NFC App</a>', unsafe_allow_html=True)
    
    # Technical details section
    with st.expander("Technical Details"):
        st.markdown("""
        ### How this works
        
        This app uses the Web NFC API, which allows web applications to read from and write to NFC tags. The app is a standalone HTML file that includes:
        
        - HTML for structure
        - CSS for styling
        - JavaScript for NFC interactions
        - Complete offline functionality
        
        ### Troubleshooting
        
        If you're having issues:
        
        1. Make sure you're using Chrome for Android (version 89+)
        2. Ensure NFC is enabled in your phone settings
        3. The app must be loaded over HTTPS (which Streamlit provides)
        4. Your device must have NFC hardware
        
        ### Data Storage
        
        All data is stored directly on the NFC tags. No data is sent to any server.
        """)
        
    # Download option
    st.download_button(
        label="Download HTML File",
        data=html_content,
        file_name="nfc_tracker.html",
        mime="text/html"
    )

if __name__ == "__main__":
    main()