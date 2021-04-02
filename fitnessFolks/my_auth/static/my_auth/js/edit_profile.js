// Change the mestrual_cycle and med_reason fields 
// based on the response of gender and ongoing_med field

document.addEventListener("DOMContentLoaded", () => {
	const ongoing_med = document.querySelector('#id_med');
	const options = document.querySelectorAll('#id_med option');
	const reason_field = document.querySelector('.col-md-12');


	const gender = document.querySelector('#id_gender');
	const gender_options = document.querySelectorAll('#id_gender option');
	const menstrual = document.querySelector('.menstrual');

	const changeReasonField = () => {
		const field = document.querySelector('.col-md-12');
		if (ongoing_med.value == "Yes") {
			if (field == null) {
				ongoing_med.parentNode.parentNode.append(reason_field);
			}
		}
		else {
			if (field != null) {
				ongoing_med.parentNode.parentNode.removeChild(reason_field);
			}
		}
	}

	const changeMenstrualField = () => {
		console.log("here");
		const field = document.querySelector('.menstrual');
		if(gender.value != "1") {
			if(field == null) {
				gender.parentNode.parentNode.append(menstrual);
			}
		}
		else {
			if(field != null) {
				gender.parentNode.parentNode.removeChild(menstrual);
			}
		}
	}

	changeReasonField();
	changeMenstrualField();

	options.forEach(option => {
		option.onclick = changeReasonField;
	});

	gender_options.forEach(option => {
		option.onclick = changeMenstrualField;
	});
});