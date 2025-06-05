from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String
from datetime import datetime
from flask_scss import Scss


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
# initialize the app with the extension
db = SQLAlchemy(app)


#Data Class
class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(300))
    complete: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=None))

    def __repr__(self):
        return f"""<b>Task #{self.id}</b>
Created at: {self.created_at}
Complite: {self.complete}
Content: {self.content}"""

with app.app_context():
        db.create_all()
        
#Home page
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Task(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        tasks_list = Task.query.order_by(Task.created_at).all()
        return render_template("index.html", tasks=tasks_list)


#delete handler
@app.route(f"/delete/<int:id>")
def delete_task(id: int):
    choosed_task = Task.query.get_or_404(id)
    try:
        db.session.delete(choosed_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
    
#update handler
@app.route(f"/edit/<int:id>", methods=["GET", "POST"])
def update_task(id: int):
    choosed_task = Task.query.get_or_404(id)
    if request.method == "POST":
        print(request.form)
        choosed_task.content = request.form["content"]
        
        try:
            if request.form["complete"] == "True":
                choosed_task.complete = True
        except:
            choosed_task.complete = False
            
        print(choosed_task.complete)    
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template("edit_form.html", task=choosed_task)


@app.route("/test")
def get_test_page():
    return render_template("ordinary.html")

if __name__ == "__main__":
        app.run(debug=True)


