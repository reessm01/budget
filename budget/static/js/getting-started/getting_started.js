//  modules already loaded in browser:
// 		@component: chartjs,
// 		@base: jquery

$(document).ready(function () {
	function customizeForms() {
		$(":input").each(function () {
			const classDict = {
				text: "form-control",
				number: "form-control",
				selectone: "custom-select",
				checkbox: "form-check-input",
			};
			const input = $(this);
			const key = input[0].type.replace("-", "");
			if (Object.keys(classDict).includes(key))
				input.addClass(classDict[key]);
		});
	}
	customizeForms();
});
