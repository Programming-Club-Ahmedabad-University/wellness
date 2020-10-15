document.addEventListener('DOMContentLoaded', () => {
	const buttons = document.querySelectorAll('.accordion-button');

	buttons.forEach( button => {
		button.onclick = () => {
			button.classList.toggle('active');
			console.log(button);
		};
	});	
})