float radius = 100;
float min_dist = radius*.656;

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
    fill(255);
    ellipse(x, y, 10, 10);
    noFill();
    ellipse(x, y, radius*2, radius*2);
  }
}

void setup(){
  size(1000,1000);
}

ArrayList<Point> list = new ArrayList<Point>();
Point active = null;

void draw(){
  background(100);
  for (Point p : list){
    p.display();
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
  }
  if(active != null && mousePressed){
    active.x = mouseX;
    active.y = mouseY;
  }
}

void mouseClicked(){
  list.add(new Point(mouseX, mouseY));
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
  float comx = 0;
  float comy = 0;
  for(Point p : list){
    comx += p.x;
    comy += p.y;
  }
  comx /= list.size();
  comy /= list.size();
  try{
  FileWriter writer = new FileWriter("/home/ben/points.txt");
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
