library(maptools)

plot.heat <- function(counties.map,state.map,z,title=NULL,breaks=NULL,reverse=FALSE,cex.legend=1,bw=.2,col.vec=NULL,plot.legend=TRUE) {
  ##Break down the value variable
  if (is.null(breaks)) {
    breaks=
      seq(
        floor(min(counties.map@data[,z],na.rm=TRUE)*10)/10
        ,
        ceiling(max(counties.map@data[,z],na.rm=TRUE)*10)/10
        ,.1)
  }
  counties.map@data$zCat <- cut(counties.map@data[,z],breaks,include.lowest=TRUE)
  cutpoints <- levels(counties.map@data$zCat)
  if (is.null(col.vec)) col.vec <- heat.colors(length(levels(counties.map@data$zCat)))
  if (reverse) {
    cutpointsColors <- rev(col.vec)
  } else {
    cutpointsColors <- col.vec
  }
  levels(counties.map@data$zCat) <- cutpointsColors
  plot(counties.map,border=gray(.8), lwd=bw,axes = FALSE, las = 1,col=as.character(counties.map@data$zCat))
  if (!is.null(state.map)) {
    plot(state.map,add=TRUE,lwd=1)
  }
  ##with(counties.map.c,text(x,y,name,cex=0.75))
  if (plot.legend) legend("bottomleft", cutpoints, fill = cutpointsColors,bty="n",title=title,cex=cex.legend)
  ##title("Cartogram")
}

##substitute your shapefiles here
state.map <- readShapeSpatial("maps/st24_d00.shp")
zip.map <- readShapeSpatial("maps/zt24_d00.shp")
## this is the variable we will be plotting
zip.map@data$noise <- rnorm(nrow(zip.map@data))
## put the lab point x y locations of the zip codes in the data frame for easy retrieval
labelpos <- data.frame(do.call(rbind, lapply(zip.map@polygons, function(x) x@labpt)))
names(labelpos) <- c("x","y")                        
zip.map@data <- data.frame(zip.map@data, labelpos)
## plot it
png(file="map.png")
## plot colors
plot.heat(zip.map,state.map,z="noise",breaks=c(-Inf,-2,-1,0,1,2,Inf))
## plot text
with(zip.map@data[sample(1:nrow(zip.map@data), 10),] , text(x,y,NAME))
dev.off()