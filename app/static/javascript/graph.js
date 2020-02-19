$(document).ready(function() {
	$(chart1).highcharts({
		chart:  args1.chart,
		title:  args1.title,
		xAxis:  args1.xAxis,
		yAxis:  args1.yAxis,
		series: args1.series
	});

	$(chart2).highcharts({
		chart:  args2.chart,
		title:  args2.title,
		xAxis:  args2.xAxis,
		yAxis:  args2.yAxis,
		series: args2.series
	});
});


