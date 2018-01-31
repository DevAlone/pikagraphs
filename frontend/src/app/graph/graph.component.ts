import { Component, OnInit, Input, ViewChild, ElementRef } from '@angular/core';
import { GraphService } from '../graph.service';

declare var document: any;
declare var AmCharts: any;


@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {
	@Input()
	graphType: string;
	@Input()
	graphId: string;
	@ViewChild('graphWrapper')
	graphWrapper: ElementRef;

	data: any[] = [];

	constructor(private graphService: GraphService) { }

	ngOnInit() {
		var self = this;
		this.graphService.getGraph(this.graphType, this.graphId).subscribe(result => {
			if (result.results && result.results.length) {
				self.data = result.results;
				self.renderGraph(self.data);
			}
		});
	}

	renderGraph(data) {
		var graphElement = document.createElement('div');
		this.graphWrapper.nativeElement.appendChild(graphElement);
		graphElement.className = 'graphElement';

        for(var i = 0; i < data.length; ++i) 
            data[i].date = data[i].timestamp * 1000;

        var chart = AmCharts.makeChart(graphElement, {
            "type": "serial",
            "theme": "light",
            "marginRight": 80,
            "autoMarginOffset": 20,
            "marginTop": 7,
            "dataProvider": data,
            "valueAxes": [{
                /*"axisAlpha": 0.2,
                "dashLength": 1,*/
                "position": "left"
            }],
            "mouseWheelZoomEnabled": false,
            "graphs": [{
                "id": "g1",
                "balloonText": "[[value]]",
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "bulletColor": "#FFFFFF",
                "hideBulletsCount": 50,
                "title": "red line",
                "valueField": "value",
                "useLineColorForBulletBorder": true,
                "balloon":{
                    "drop":true
                }
            }],
            "chartScrollbar": {
                "autoGridCount": true,
                "graph": "g1",
                "scrollbarHeight": 40
            },
            "chartCursor": {
               "limitToGraph":"g1"
            },
            "categoryField": "date",
            "categoryAxis": {
                "minPeriod": "mm",
                "parseDates": true,
                "axisColor": "#DADADA",
                "dashLength": 1,
                "minorGridEnabled": true
            },
            "export": {
                "enabled": true
            }
        });

        chart.addListener("rendered", zoomChart);
        zoomChart();

        // this method is called when chart is first inited as we listen for "rendered" event
        function zoomChart() {
            // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
            chart.zoomToIndexes(data.length - 40, data.length - 1);
        }
    }
}
