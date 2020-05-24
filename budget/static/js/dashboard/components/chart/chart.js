// modules already loaded in browser: chartjs, jquery

export class ChartClient {
	tracker = 0;
	datas = {}

	constructor(datas) {
		this.datas = datas;
	}

	loadChart() {
		let titleList = this.datas[this.tracker].title.split("_");
		for (let index in titleList) {
			let word = titleList[index];
			word =
				word.charAt(0).toUpperCase() +
				word.substr(1).toLowerCase();
			titleList[index] = word;
		}
		const title = titleList.join(" ");
		var chart = new CanvasJS.Chart("chart", {
			animationEnabled: true,
			title: {
				text: title,
			},
			data: [
				{
					type: "pie",
					startAngle: 240,
					yValueFormatString:
						'##0.00"%"',
					indexLabel: "{label} {y}",
					dataPoints: this.datas[
						this.tracker
					].data,
				},
			],
		});
		chart.render();
	}

	removeActive(n) {
		$(`#list${n}`).removeClass();
	}

	addActive(n) {
		$(`#list${n}`).addClass("active");
	}

	determineIndex(n) {
		if (
			this.tracker + n >= 0 &&
			this.tracker + n < this.datas.length
		)
			this.tracker += n;
		else if (this.tracker + n < 0)
			this.tracker = this.datas.length - 1;
		else this.tracker = 0;
	}

	refreshChart() {
		$("#chart").remove();
		$("#chartParent").append(
			`<div id="chart" class="chart"></div>`
		);

		this.loadChart();
	}

	selectSlide(e) {
		const id = parseInt(e.target.id.replace(/\D/g, ""));
		this.removeActive(this.tracker);
		this.tracker = id;
		this.loadChart();
		this.addActive(this.tracker);
	}

	switchSlides(n) {
		this.removeActive(this.tracker);
		this.determineIndex(n);
		this.addActive(this.tracker);
		this.refreshChart();
	}
}
