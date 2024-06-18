async function func(hasEncrypt){
    const fileInput = document.getElementById('file-input');
    const selectedFile = fileInput.files[0];

    const downloadLink = document.getElementById('download-link');

    const srcText = document.getElementById('src');
    const srcType = document.getElementById('srcType').value;

    const modeSelect = document.getElementById('mode').value;
    const iv = document.getElementById('IV').value;

    const paddingSelect = document.getElementById('padding').value;

    const keySize = document.getElementById('keySize').value;
    const key = document.getElementById('key').value;

    const outputText = document.getElementById('output');
    const outType = document.getElementById('outType');


    if (! checkArgs(key, keySize, iv, modeSelect)){
        return
    }

    if (selectedFile){
        console.log("File selected: ",selectedFile.name);
        
        const reader = new FileReader();
        reader.onload = function(event) {
            var fileContent = event.target.result;

            var it = "UTF8", ot="BASE64";
            if (!hasEncrypt){
                it = "BASE64";
                ot = "UTF8";
                fileContent = binaryToBase64(fileContent)
            }
            const payload = {
                "keySize": keySize,
                "padding": paddingSelect.toUpperCase(),
                "mode": modeSelect.toUpperCase(),
                "iv": iv,
                "input": fileContent,
                "inputType": it.toUpperCase(),
                "outputType": ot.toUpperCase(),
                "key": key,
                "encrypt": hasEncrypt
            }

            console.log(payload);
            postToAesEndpoint(payload)
            .then(data =>{

                console.log(data);
                downloadLink.style.display = "block";
                if (hasEncrypt){
                    const binaryString = base64ToBinary(data.output);
                    const blob = new Blob([binaryString], { type: 'text/plain' });
                    downloadLink.href = URL.createObjectURL(blob);
                    downloadLink.download = 'encrypted_'+selectedFile.name;
                }else{
                    const blob = new Blob([data.output], { type: 'text/plain; charset=UTF-8' });
                    downloadLink.href = URL.createObjectURL(blob);
                    downloadLink.download = 'decrypted_'+selectedFile.name;
                }

                downloadLink.innerHTML = 'Tải file output!';
            })
        };

        reader.readAsText(selectedFile, 'UTF-8');
     
    }else {
        if (srcText.value.length != 0){
            console.log("de/en ",srcText.value);

            const payload = {
                "keySize": keySize,
                "padding": paddingSelect.toUpperCase(),
                "mode": modeSelect.toUpperCase(),
                "iv": iv,
                "input": srcText.value,
                "inputType": srcType.toUpperCase(),
                "outputType": outType.value.toUpperCase(),
                "key": key,
                "encrypt": hasEncrypt
            }

            console.log(payload);

            postToAesEndpoint(payload)
            .then(data =>{
                outputText.value = data.output;
                outType.value = data.outputType;
            })
        }else{
            alert("Không có input!")            
            console.error("no input");
        }
        downloadLink.style.display = "none";
    } 
}

function binaryToBase64(binaryString) {
    var byteCharacters = binaryString.match(/.{1,8}/g); // Chia nhỏ thành từng byte (8 ký tự)
    var byteNumbers = byteCharacters.map(function(byte) {
        return parseInt(byte, 2);
    });
    
    var byteArray = new Uint8Array(byteNumbers);
    
    var base64String = btoa(String.fromCharCode.apply(null, byteArray));
    
    return base64String;
}

function base64ToBinary(base64String) {
    var binaryString = atob(base64String);
    var binary = "";
    for (var i = 0; i < binaryString.length; i++) {
        var charCode = binaryString.charCodeAt(i).toString(2);
        var paddedByte = '0'.repeat(8 - charCode.length) + charCode;
        binary += paddedByte;
    }
    
    return binary;
}

async function postToAesEndpoint(payload) {
    return await fetch('/aes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response=> response.json())
}

function checkArgs(key, keySize, iv, mode){
    const encoder = new TextEncoder();
    const requiredBytes = parseInt(keySize) / 8;
    const keyBytes = encoder.encode(key).length;

    console.log(keyBytes, " ", requiredBytes);
    // check key size and key input length 
    if (keyBytes != requiredBytes) {
        alert("Khoá không phù hợp!")
        console.error("no key");
        return false
    }

    console.log(iv.length, ' ', mode);
    // check iv input length
    if (iv.length != 16 && mode != "ecb") {
        alert("Thiếu giá trị IV!")
        console.error("no iv");
        return false
    }
    return true
}

document.addEventListener('DOMContentLoaded', function() {
    const modeSelect = document.getElementById('mode');
    const iv = document.getElementById('IV');
    const keySize = document.getElementById('keySize');
    const key = document.getElementById('key');

    // change mode -> display or hide iv input
    modeSelect.addEventListener('change', function() {
        if (modeSelect.value === 'ecb') {
            iv.style.display = 'none';
        } else {
            iv.style.display = 'block';
        }
    });

    // change key size -> change max length input key
    keySize.addEventListener('change', function() {
        if (keySize.value === '128') {
            key.maxLength = 16;
        } else if (keySize.value === '192') {
            key.maxLength = 24;
        } else{
            key.maxLength = 32;
        }
    });
});
