// Calculator functionality for IronBeast Gym Website

document.addEventListener('DOMContentLoaded', function() {
    // TDEE Calculator Form
    const tdeeForm = document.getElementById('tdee-calculator');
    
    if (tdeeForm) {
        tdeeForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Get form values
            const weight = parseFloat(document.getElementById('weight').value);
            const height = parseFloat(document.getElementById('height').value);
            const age = parseInt(document.getElementById('age').value);
            const gender = document.getElementById('gender').value;
            const activityLevel = document.getElementById('activity-level').value;
            
            // Validation
            if (isNaN(weight) || isNaN(height) || isNaN(age) || weight <= 0 || height <= 0 || age <= 0) {
                showError('Please enter valid values for weight, height, and age.');
                return;
            }
            
            // Send data to the server for calculation
            fetch('/calculate-tdee', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    weight: weight,
                    height: height,
                    age: age,
                    gender: gender,
                    activityLevel: activityLevel
                }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error:', error);
                showError('There was an error calculating your results. Please try again.');
            });
        });
    }
    
    // Function to display calculation results
    function displayResults(data) {
        const resultsDiv = document.getElementById('calculator-results');
        
        if (resultsDiv) {
            resultsDiv.innerHTML = `
                <div class="p-4 golden-card rounded-lg mt-6 mb-6">
                    <h3 class="text-xl font-bold mb-2 golden-text">Your Results</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="p-3 bg-black rounded border border-yellow-600">
                            <p class="text-sm text-gray-400">BMR (Basal Metabolic Rate):</p>
                            <p class="text-2xl golden-text">${data.bmr} calories</p>
                            <p class="text-xs text-gray-500">Calories your body needs at complete rest</p>
                        </div>
                        <div class="p-3 bg-black rounded border border-yellow-600">
                            <p class="text-sm text-gray-400">TDEE (Total Daily Energy Expenditure):</p>
                            <p class="text-2xl golden-text">${data.tdee} calories</p>
                            <p class="text-xs text-gray-500">Calories your body needs per day with your activity level</p>
                        </div>
                    </div>
                    <div class="mt-4 p-3 bg-black rounded border border-yellow-600">
                        <p class="text-sm text-gray-400">Recommended Daily Protein Intake:</p>
                        <p class="text-2xl golden-text">${data.protein_min} - ${data.protein_max} grams</p>
                        <p class="text-xs text-gray-500">Based on your body weight (0.8g - 1.2g per pound)</p>
                    </div>
                    <div class="mt-4">
                        <h4 class="font-semibold golden-text mb-2">What Do These Numbers Mean?</h4>
                        <ul class="text-sm text-gray-300 list-disc pl-5">
                            <li>To <span class="text-green-400">gain weight</span>, eat 300-500 calories above your TDEE</li>
                            <li>To <span class="text-red-400">lose weight</span>, eat 300-500 calories below your TDEE</li>
                            <li>To <span class="text-blue-400">maintain weight</span>, eat at your TDEE</li>
                            <li>Consume adequate protein to build and repair muscle tissue</li>
                        </ul>
                    </div>
                </div>
            `;
            
            // Scroll to results
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
    }
    
    // Function to show error messages
    function showError(message) {
        const errorDiv = document.getElementById('calculator-error');
        
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.remove('hidden');
            
            // Hide error after 5 seconds
            setTimeout(() => {
                errorDiv.classList.add('hidden');
            }, 5000);
        }
    }
    
    // Calorie tracking form
    const trackingForm = document.getElementById('calorie-tracking-form');
    
    if (trackingForm) {
        trackingForm.addEventListener('submit', function(event) {
            // Form submission is handled by the server, but we can add client-side validation
            const calories = parseInt(document.getElementById('calories').value);
            const protein = parseInt(document.getElementById('protein').value);
            
            if (isNaN(calories) || isNaN(protein) || calories < 0 || protein < 0) {
                event.preventDefault();
                alert('Please enter valid values for calories and protein.');
            }
        });
    }
});
