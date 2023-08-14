	const translations ={
		"Job-Application.AI": "Bewerbungen.AI",
		"Full Name": "Name",
		"Name of the company": "Name des Unternehmens",
		"Position": "Position",
		"Sector": "Branche",
		"Position now (leave empty if you are not working)": 'Aktuelle Position (leer lassen, wenn Sie nicht arbeiten)',
    "Company now (leave empty if you are not working)": "Aktuelles Unternehmen (leer lassen, wenn Sie nicht arbeiten)",
		"Education": "Ausbildung",
		"Skills": "Fähigkeiten",
		"Work experience": "Berufserfahrung",
		"Achievements": "Erfolge",
		"Side Projects": "Nebenprojekte",
		"Job description": "Stellenbeschreibung",
		"Submit": "Einreichen",
		"Translate to German": "Translate to English"
	};

	function translate() {
	    const mainHeading = document.getElementById("mainHeading");
	    const labels = document.querySelectorAll("label");
	    const buttons = document.querySelectorAll("button");

	    if (mainHeading.textContent === "Job-Application.AI") {
		mainHeading.textContent = translations[mainHeading.textContent];
		labels.forEach(label => {
			label.textContent = translations[label.textContent];
		});
		buttons.forEach(button =>{
			button.textContent = translations[button.textContent];
		})
	    } else {
		const keysAr = Object.keys(translations)
		mainHeading.textContent = keysAr[0];
		labels.forEach(label => {
		    for (const key in translations) {
			if (translations[key] === label.textContent) {
			    	label.textContent = key;
			}
		    }
		});
		buttons.forEach(button => {
		    for (const key in translations) {
			if (translations[key] === button.textContent) {
			    	button.textContent = key;
			}
		    }
	    })
	}
	}

	function clean(){
		const inputs = document.querySelectorAll("input");
		inputs.forEach(input =>{
			input.value = "";
		})
		const areas = document.querySelectorAll("textarea")
		areas.forEach(area =>{
			area.textContent = "";
		})
	}

	document.addEventListener("DOMContentLoaded", function() {
    		const btnTranslate = document.getElementById("btnTranslate");
    		btnTranslate.onclick = translate;
		    btnClean.onclick = clean
	});
