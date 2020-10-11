document.addEventListener("DOMContentLoaded", () => {
	const ongoing_med = document.querySelector('#id_ongoing_med');
	const options = document.querySelectorAll('#id_ongoing_med option');
	const reason_field = document.querySelector('.col-md-12');

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

	changeReasonField();

	options.forEach(option => {
		option.onclick = changeReasonField;
	});
});