$(document).ready(function () {
	function getTitle(key) {
		const answerKey = {
			title:
				"Label describing item. Use names you can easily remember.",
			amount:
				"Amount of representing balance earned, owed or accrued.",
			frequency: "How frequently does this occur?",
			last_paid: "The last time payment was dispersed.",
			weekdays_only:
				"Check this if the payment does not post on the weekend.",
			account_type:
				"Type or category the account belongs to.",
			action: "Save changes or delete entry.",
		};
		if (Object.keys(answerKey).includes(key))
			return answerKey[key];
		else return "";
	}

	function assignToolTipMessage() {
		const keys = [
			"title",
			"amount",
			"frequency",
			"last_paid",
			"weekdays_only",
			"account_type",
			"action",
		];

		for (let i in keys) {
			$(`.tooltip-${keys[i]}`)
				.data("bs.tooltip", false)
				.tooltip({ title: getTitle(keys[i]) });
		}
	}

	assignToolTipMessage();
});
