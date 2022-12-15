// <!-- Resources -->
document.write('<script src="https://cdn.amcharts.com/lib/5/index.js"></script>')
document.write('<script src="https://cdn.amcharts.com/lib/5/xy.js"></script>')
document.write('<script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>')


window.onload=function() {
    am5.ready(function() {
        // Create root element
        // https://www.amcharts.com/docs/v5/getting-started/#Root_element
        var root = am5.Root.new("chartdiv");
    
        
        // Set themes
        // https://www.amcharts.com/docs/v5/concepts/themes/
        root.setThemes([
          am5themes_Animated.new(root),
          //am5themes_Dark.new(root),
        ]);
    
        // 색상변경
        root.interfaceColors.setAll({
          grid: am5.color("#fff"),
          text: am5.color("#ced4da"),
        })
    
        
        // Create chart
        // https://www.amcharts.com/docs/v5/charts/xy-chart/
        var chart = root.container.children.push(am5xy.XYChart.new(root, {
          panX: true,
          panY: true,
          wheelX: "panX",
          wheelY: "zoomX",
          pinchZoomX:true,
          
        }));
        
        
        // Add cursor
        // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
        var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {
          behavior: "none",
        }));
        cursor.lineY.set("visible", false);
    
        
    
    
    
        // Generate random data
        var date = new Date();
        date.setHours(0, 0, 0, 0);
        var value = 100;
        
        function generateData() {
          value = Math.round((Math.random() * 10 - 5) + value);
          am5.time.add(date, "hour", 1);
          return {
            date: date.getTime(),
            value: value
          };
        }
        
        function generateDatas(count) {
          var data = [];
          for (var i = 0; i < count; ++i) {
            data.push(generateData());
          }
          return data;
        }
    
        // data 생성
        var data = generateDatas(1200);
    
        // data 의 평균 구하기
        let DataArray=[]
        for (d of data){
          DataArray.push(d.value)
        }
        let sumDataArray = DataArray.reduce((a, b) => a + b)
        let AvgData = sumDataArray / DataArray.length
    
        
    
        
        
        // Create axes
        // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
         var xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
           maxDeviation: 0.2,
           baseInterval: {
             timeUnit: "hour",
             count: 1
           },
          tooltipDateFormat: "yyyy.MM.dd HH:mm",
          renderer: am5xy.AxisRendererX.new(root, {}),
          tooltip: am5.Tooltip.new(root, {})
        }));
    
        var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
          baseValue: AvgData , // 위쪽 fill 기준선 정하기 
          renderer: am5xy.AxisRendererY.new(root, {})
        }));
        
        
        // Add series
        // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
        var series = chart.series.push(am5xy.SmoothedXLineSeries.new(root, {
          name: "Series",
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: "value",
          valueXField: "date",
          tooltip: am5.Tooltip.new(root, {
            labelText: "[bold]{valueY}"
          }),
        }));
        series.strokes.template.setAll({
          strokeWidth: 2
        });
        series.fills.template.setAll({
          visible: true,
          fillOpacity: 0.1
        });
    
    
        var rangeDate = new Date();
        am5.time.add(rangeDate, "hour", Math.round(series.dataItems.length / 2))
        var rangeTime = rangeDate.getTime();
    
        // add series range
        var seriesRangeDataItem = yAxis.makeDataItem({ value: -999, endValue: AvgData });
        var seriesRange = series.createAxisRange(seriesRangeDataItem);
        seriesRange.fills.template.setAll({
          fill: am5.color(0xff621f),
          fillOpacity: 0.1,
          visible: true
        });
        seriesRange.strokes.template.setAll({
          stroke: am5.color(0xff621f),
        });
    
        seriesRangeDataItem.get("grid").setAll({
          location: 1,
          strokeOpacity: 1,
          visible: true,
          stroke: am5.color('#fff'),
          strokeWidth : 2,
          strokeDasharray: [10, 4]
        })
    
        seriesRangeDataItem.get("label").setAll({
          location: 1,
          visible:true,
          text:"avg",
          inside:true,
          centerX:0,
          centerY:am5.p100,
          fontWeight:"bold",
        })
        
        
        // Add scrollbar
        var scrollbar = chart.set("scrollbarX", am5.Scrollbar.new(root, {
          orientation: "horizontal"
        }));
        chart.bottomAxesContainer.children.push(scrollbar);
    
    
        
        // Set data
        series.data.setAll(data);
    
        // Make stuff animate on load
        // https://www.amcharts.com/docs/v5/concepts/animations/
        series.appear(1000);
        chart.appear(1000, 100);
    
    
        //set tooltip
        var tooltipBullet = chart.plotContainer.children.push(am5.Circle.new(root, {
          radius: 5,
          fill: series.get("fill"),
          x: -1000,
          width: am5.percent(60)
        }));
    
        series.on("tooltipDataItem", function(tooltipDataItem) {
          var x = -1000;
          var y = -1000;
          if (tooltipDataItem) {
            var point = tooltipDataItem.get("point");
            if (point) {
              x = point.x;
              y = point.y;
            }
          }
          tooltipBullet.setAll({
            x: x,
            y: y
          })
        });
    
        tooltip.on("opacity", function(opacity){
          tooltipBullet.set("opacity", opacity);
        });
        
      }); // end am5.ready()
}

