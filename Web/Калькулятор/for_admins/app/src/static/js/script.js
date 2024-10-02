function appendValue(value) {
    const display = document.getElementById('display');
    if (display.innerText === '0') {
        display.innerText = value;
    } else {
        display.innerText += value;
    }
}

function clearDisplay() {
    document.getElementById('display').innerText = '0';
}

async function calculate() {
    const expression = document.getElementById('display').innerText;

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expression })
        });

        const result = await response.json();
        document.getElementById('display').innerText = result.result;
    } catch (error) {
        document.getElementById('display').innerText = 'Error';
    }
}
