var c = svg.selectAll("circle")
            .data(data).enter()
            .append("circle")
            .attr("cx", function(d) {
                return d["x"]+200;
        })
            .attr("cy", function(d) {
                return 150;
        })
            .attr("r", function(d) {
                return 120;
        })
            .attr("fill", "#385280")
            //.attr("stroke-width", "15")
            //.attr("stroke", "#385280")
        ;
            
c.on("mouseover", function (d){
            var circleUnderMouse = this; 
            c.transition()
                .attr('fill-opacity',function () {
                    return (this === circleUnderMouse) 
                    ? "100%" : "5%"})
    
            text1 = d["t3"]
            text2 = d["t4"]
            p1.transition()
                .text(text1)
                .attr("x",function() {
                    return (d["t2"]==='positions') ? 100:380})
                .attr('opacity',"100%")
                .attr("font-weight", "bolder")
    
            p2.transition()
                .text(text2)
                .attr("x",function() {
                    return (d["t2"]==='positions') ? 100:280})
                .attr('opacity',"100%")

        });

c.on("mouseout", function (d){
            c.transition()
                .attr('fill-opacity',"100%")
    
            p1.transition()
                .attr("x", 550)
                .attr("opacity", "50%")
                .attr("font-weight", "lighter")
                .text("Hover on a circle to view details")
            
            p2.transition().attr('opacity',"0%")
    
        });

var t = svg.selectAll("text")
            .data(data).enter()
            .append("text")
            .attr("x", function(d) {
                return d["x"]+200;
        })
            .attr("y", function(d) {
                return 150;
        })
            .text(function (d) {
                return d["t1"] 
                
        })
            .attr("text-anchor", "middle")
            .attr("font-weight","bold")
            .attr("font-size", "50px")
            .attr("fill", "white");

t.append("tspan")
            .attr("x", function(d) {
                return d["x"]+200;
        })
            .attr("y", function(d) {
                return 200;
        })
            .text(function (d) {
                return d["t2"] 
                
        })
            .attr("text-anchor", "middle")
            .attr("font-weight","normal")
            .attr("font-size", "25px")
            .attr("fill", "white");

var p1 = svg.append("text")
        .attr("x", 550)
        .attr("y", 350)
        .attr("opacity", "50%")
        .attr("font-size", "16px")
        .attr("text-align", "left")
        .attr("font-weight", "lighter")
        .attr("font-style", "italic")
        .text("Hover on a circle to view details");

var p2 = svg.append("text")
        .attr("y", 380)
        .attr("opacity", "0%")
        .attr("font-size", "16px")
        .attr("text-align", "middle")
        .attr("background-color", "green")
        .attr("font-weight","bolder")
        .attr("font-style","italic");



d3.select("#d3").style("height","420px");
