import {Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';
import {GraphService} from '../graph.service';
import {LoadingAnimationService} from '../loading-animation.service';

declare var document: any;
declare var AmCharts: any;


@Component({
    selector: 'app-bar-chart',
    templateUrl: './bar-chart.component.html',
    styleUrls: ['./bar-chart.component.css']
})
export class BarChartComponent implements OnInit {
  @Input()
  graphType: string;
  @Input()
  graphId: string;
  @Input()
  windowSize = 100;
  @Input()
  isLogarithmic = false;
  @ViewChild('graphWrapper')
  graphWrapper: ElementRef;

  data: any[] = [];

  constructor(private graphService: GraphService,
              private loadingAnimationService: LoadingAnimationService) { }

  ngOnInit() {
    this.graphId += '?window_size=' + this.windowSize;
    this.loadingAnimationService.start();
    this.graphService.getGraph(this.graphType, this.graphId).subscribe(result => {
      this.loadingAnimationService.stop();
      if (result.data && result.data.length) {
        this.data = result.data;
        this.renderGraph(this.data);
      }
    });
  }

  renderGraph(data) {
    const graphElement = document.createElement('div');
    this.graphWrapper.nativeElement.appendChild(graphElement);
    graphElement.className = 'graphElement';
    // for (let i = 0; i < data.length; ++i) {
    //   data[i].x = data[i].x;
    // }

    const chart = AmCharts.makeChart(graphElement, {
      'type': 'serial',
      'theme': 'light',
      'marginRight': 70,
      'dataProvider': this.data,
      'valueAxes': [{
        'logarithmic': this.isLogarithmic,
        'axisAlpha': 0,
        'position': 'left',
        // 'title': ''
      }],
      'startDuration': 1,
      'graphs': [{
        'id': 'g1',
        'balloonText': '<b>[[category]]: [[value]]</b>',
        // 'fillColorsField': 'color',
        'fillAlphas': 0.9,
        'lineAlpha': 0.2,
        'type': 'column',
        'valueField': 'y'
      }],
      'chartScrollbar': {
        'autoGridCount': true,
        'graph': 'g1',
        'scrollbarHeight': 40
      },
      'chartCursor': {
        'categoryBalloonEnabled': false,
        'cursorAlpha': 0,
        'zoomable': false
      },
      'categoryField': 'x',
      'categoryAxis': {
        'gridPosition': 'start',
        'labelRotation': 45
      },
      'export': {
        'enabled': true
      }
    });
    chart.addListener('rendered', zoomChart);
    zoomChart();
    // this method is called when chart is first inited as we listen for 'rendered' event
    function zoomChart() {
      // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
      chart.zoomToIndexes(data.length - 40, data.length - 1);
    }
  }
}
