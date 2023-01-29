float radius = 50;
float min_dist = radius*.656;

String SAVE_PATH = "/home/ben/points.txt";

import java.io.FileWriter;
import java.util.stream.Collectors;

class Point{
  float x;
  float y;
  Point(float xpos, float ypos){
    x = xpos;
    y = ypos;
  }
  
  void display(){
    fill(0);
    ellipse(x, y, 10, 10);
  }
}

void setup(){
  size(800,800);
  textSize(20);
  stroke(0);
}

ArrayList<Point> list = new ArrayList<Point>();
Point active = null;

void draw(){
  background(255);
  stroke(255,0,0);
  noFill();
  rect(0,0,74/6.1*radius, 75/6.1*radius);
  text(list.size(),20,20);
  for (Point p : list){
    p.display();
    stroke(0);
    for (Point q : list){
      if(dist(q.x,q.y, p.x,p.y)<radius && q != p){
        if(dist(q.x,q.y, p.x,p.y) < min_dist){
          stroke(255,0,0);
        }else{
         stroke(0);
        }
        line(q.x,q.y,p.x,p.y);
      }
    }
    if(p == active){
        noFill();
        ellipse(p.x, p.y, radius*2, radius*2);
    }
  }
  if(active != null && mousePressed){
    active.x = mouseX;
    active.y = round(mouseY/min_dist)*min_dist;
  }
}

void mouseClicked(){
  list.add(new Point(mouseX, round(mouseY/min_dist)*min_dist));
}

void mousePressed(){
  if(active == null){
    for (Point p : list){
      print(dist(p.x, p.y, mouseX, mouseY));
      if(dist(p.x, p.y, mouseX, mouseY)<10){
        active = p;
        break;
      }
    }
  }else{
    if(dist(mouseX, mouseY, active.x,active.y) > radius){
      active = null;
    }
  }
}

void keyPressed(){
  if(key=='m'){
    list.remove(list.size()-1);
    return;
  }
  float comx = 0;
  float comy = 0;
  for(Point p : list){
    comx += p.x;
    comy += p.y;
  }
  comx /= list.size();
  comy /= list.size();
  try{
  FileWriter writer = new FileWriter(SAVE_PATH);
  String pts = "";
  for (Point pt : list){
    pts = pts + "("+String.valueOf((pt.x-comx)/radius) + "," + String.valueOf((pt.y-comy)/radius)+"),\n";
  }
  writer.write(pts); 
  writer.close();
  }catch(IOException ex){print(ex);}

}
  
void mouseReleased(){
    active = null;
}
