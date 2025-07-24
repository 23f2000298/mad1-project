# from flask import Flask,render_template,redirect,request,session
# import math
# import pytz
# from flask import current_app as app #if we do directly import then it will lead to circular flow
# #current _app refers to app object tsht we created
# from .models import *
# import os
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt
# from collections import Counter


# @app.route("/",methods = ["GET","POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form.get("password")
#         this_user = User.query.filter_by(username = username).first() #lhs >> table,rhs>>form data
#         parkinglots = ParkingLot.query.all()
#         if this_user:
#             if this_user.password  == password:
#                 session["user_id"] = this_user.id
#                 if this_user.type == "admin":
#                     lot_info = []
#                     for lot in parkinglots:
#                         total_spots = lot.maximum_spot
#                         booked = Booking.query.filter_by(lot_id = lot.id).count()
#                         available = total_spots - booked
#                         lot_info.append({"id":lot.id,"name":lot.name,"address":lot.address,"available":available,"total":total_spots})
#                     return render_template("admin_dashboard.html",this_user = this_user,parkinglots = parkinglots,lot_info = lot_info)
#                 else:
#                     spots = Booking.query.filter_by(user_id = this_user.id).all()
#                     lot_info = []
#                     for lot in parkinglots:
#                         total_spots = lot.maximum_spot
#                         booked = Booking.query.filter_by(lot_id = lot.id).count()
#                         available = total_spots - booked
#                         lot_info.append({"id":lot.id,"name":lot.name,"address":lot.address,"available":available,"total":total_spots})
#                     return render_template("user_dashboard.html",this_user = this_user,spots = spots,lot_info = lot_info)
#             else:
#                 return "Password is wrong"
#         else:
#             return "user does not Exist"
        
#     return render_template("login.html")




# @app.route("/register",methods = ["GET","POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form.get("password")
#         user_name = User.query.filter_by(username = username).first()
#         user_email = User.query.filter_by(email = email).first()
#         if user_name or user_email:
#            return "user already exist"
#         else:
#             user = User(username = username,email = email,password = password)
#             db.session.add(user)
            
#             db.session.commit()
#             return redirect("/")
#     return render_template("register.html")

# @app.route("/users")
# def user():
#     users = User.query.filter_by(type = "general").all()
#     return render_template("user.html",users = users)



# @app.route("/add_parkinglot",methods = ["GET","POST"])
# def create_parkinglot():



#     this_user = User.query.filter_by(type = "admin").first()
#     parkinglots = ParkingLot.query.all()
#     if request.method == "POST":
#         name = request.form["name"]
#         address = request.form["address"]
#         pincode = request.form["pincode"]
#         price_per_hour = request.form["price_per_hour"]
#         maximum_spot = int(request.form["maximum_spot"])

#         existing_parkinglot = ParkingLot.query.filter_by(name = name).first()
#         if existing_parkinglot:
#             return "parkinglot already exist"
#         parkinglot = ParkingLot(name = name,address = address,pincode = pincode,price_per_hour = price_per_hour,maximum_spot = maximum_spot,user_id = this_user.id)
#         db.session.add(parkinglot)
#         db.session.commit()

#         parkinglots = ParkingLot.query.all()
#         lot_info = []
#         for lot in parkinglots:
#             total_spots = lot.maximum_spot
#             booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
#             available_spots = total_spots - booked_spots
#             lot_info.append({
#                 "id":lot.id,
#                 "name":lot.name,
#                 "address":lot.address,
#                 "available":available_spots,
#                 "total":total_spots
#             })
#         return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info)
#     return render_template("add_parkinglot.html",this_user = this_user,parkinglots = parkinglots)
    
# @app.route("/delete_parkinglot/<int:parkinglot_id>",methods = ["GET","POST"])
# def delete_parkinglot(parkinglot_id):
#     this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
#     bookings = Booking.query.filter_by(lot_id = this_parkinglot.id).all()
#     if bookings:
#         return "cannot delete this parkinglot because it has bookings"
#     db.session.delete(this_parkinglot)
#     db.session.commit()
#     this_user = User.query.filter_by(type = "admin").first()
#     parkinglots = ParkingLot.query.all()

#     lot_info = []
#     for lot in parkinglots:
#         total_spots = lot.maximum_spot
#         booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
#         available_spots = total_spots - booked_spots
#         lot_info.append({
#             "id":lot.id,
#             "name":lot.name,
#             "address":lot.address,
#             "available":available_spots,
#             "total":total_spots
#         })
#     return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info,parkinglots = parkinglots)
    
   


# @app.route("/edit_parkinglot/<int:parkinglot_id>",methods = ["GET","POST"])
# def edit_parkinglot(parkinglot_id):
#     this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
#     print(this_parkinglot)
#     if request.method == "POST":
#         this_parkinglot.name = request.form["name"]
#         this_parkinglot.address = request.form["address"]
#         this_parkinglot.pincode = request.form["pincode"]
#         this_parkinglot.price_per_hour = request.form["price_per_hour"]
#         this_parkinglot.maximum_spot = request.form["maximum_spot"]
#         db.session.commit()
#         this_user = User.query.filter_by(type = "admin").first()
#         parkinglots = ParkingLot.query.all()
        
#         lot_info = []
#         for lot in parkinglots:
#             total_spots = lot.maximum_spot
#             booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
#             available_spots = total_spots - booked_spots
#             lot_info.append({
#                 "id":lot.id,
#                 "name":lot.name,
#                 "address":lot.address,
#                 "available":available_spots,
#                 "total":total_spots
#             })
#         return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info)
#     return render_template("edit_parkinglot.html",this_parkinglot = this_parkinglot)


# @app.route("/view_lot/<int:parkinglot_id>",methods = ["GET","POST"])  
# def view_parkinglot(parkinglot_id):
    
#     this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
#     bookings = Booking.query.filter_by(lot_id = this_parkinglot.id).all()
#     booked_spots_ids = [booking.spot_id for booking in bookings]
#     print("booked ids",booked_spots_ids)
#     return render_template("view_lot.html",this_parkinglot = this_parkinglot,booked_spots_ids = booked_spots_ids)


# @app.route("/delete_spot/<int:parkinglot_id>/<int:spot_id>",methods = ["GET","POST"])
# def delete_spot(parkinglot_id,spot_id):
#     booking = Booking.query.filter_by(lot_id = parkinglot_id,spot_id = spot_id).first()
#     if booking:
#         return "cannot delete this spot because it has booking"
#     spot = Booking.query.filter_by(id = spot_id).first()
#     db.session.delete(spot)
#     db.session.commit()
#     return f"Spot {spot_id} deleted successfully"


# @app.route("/book/<int:parkinglot_id>/<int:user_id>",methods = ["GET","POST"])
# def book(parkinglot_id,user_id):
#     this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
#     this_user = User.query.filter_by(id = user_id).first()
#     spots = Booking.query.filter_by(lot_id = this_parkinglot.id).all()
#     if request.method == "GET":
#         existing_spots = Booking.query.filter_by(lot_id = this_parkinglot.id).count()
#         next_spot_id = existing_spots + 1
#         if next_spot_id > this_parkinglot.maximum_spot:
#             return render_template("sorry all full")
#         return render_template("book.html",this_parkinglot = this_parkinglot,this_user = this_user,next_spot_id = next_spot_id)
#     else:
#         vehicle_no = request.form["vehicle_no"]
#         spot_id = int(request.form["spot_id"])
#         lot_id = int(request.form["lot_id"])
#         user_id = int(request.form["user_id"])

#         existing_booking = Booking.query.filter_by(vehicle_no = vehicle_no).first()
#         if existing_booking:
#             return "vehicle_already_booked.html"
#         booking = Booking(vehicle_no = vehicle_no,spot_id = spot_id,lot_id = lot_id,user_id = user_id,parking_time = datetime.now())
#         # booking = Booking(vehicle_no = vehicle_no,spot_id = spot_id,lot_id = lot_id,user_id = user_id,parking_time = datetime.now(),release_time = None,available = False)  #new
#         db.session.add(booking)
#         db.session.commit()
#         spots = Booking.query.filter_by(user_id = this_user.id).all()
#         parkinglots = ParkingLot.query.all()
#         lot_info = []
#         for lot in parkinglots:
#             total_spots = lot.maximum_spot
#             booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
#             available_spots = total_spots - booked_spots
#             lot_info.append({
#                 "id":lot.id,
#                 "name":lot.name,
#                 "address":lot.address,
#                 "available":available_spots,
#                 "total":total_spots
#             })
#         # history = Booking.query.filter(Booking.user_id == this_user.id,Booking.release_time != None).all()  #new
#         return render_template("user_dashboard.html",this_user = this_user,spots = spots,lot_info = lot_info)
       

      




# @app.route("/view_spot/<int:parkinglot_id>/<int:spot_id>")
# def view_spots(parkinglot_id,spot_id):
#     lot = ParkingLot.query.get(parkinglot_id)
#     spot = Booking.query.filter_by(lot_id = lot.id,spot_id = spot_id).first()
#     if not spot or not lot:
#         return "<h1>Spot is not booked</h1>"
#     user = User.query.get(spot.user_id)
#     return render_template("single_view_spot.html",spot = spot,lot = lot,user = user)



    
# @app.route("/search")
# def search():
#     search_word = request.args.get("search")
#     key = request.args.get("key")
#     if not search_word or not key:
#         return "Please provide search word and key"
#     if key == "name":
#         results = ParkingLot.query.filter(ParkingLot.name.ilike(f"%{search_word}%")).all()
   
#     else:
#         results = ParkingLot.query.filter(ParkingLot.pincode.ilike(f"%{search_word}%")).all()
#     return render_template("result.html",results = results,key = key)


# @app.route("/admin_dashboard")
# def admin_dashboard():
#     this_user = User.query.filter_by(type = "admin").first()
    
#     parkinglots = ParkingLot.query.all() 

#     lot_info = []
#     for lot in parkinglots:
#         total_spots = lot.maximum_spot
#         booked_spots = Booking.query.filter_by(lot_id = lot.id,release_time = None).count()
#         # booked_spots = Booking.query.filter_by(lot_id = lot.id,available = False).count()  #new
#         available_spots = total_spots - booked_spots
#         lot_info.append({
#             "id":lot.id,
#             "name":lot.name,
#             "address":lot.address,
#             "available":available_spots,
#             "total":total_spots
#         })

  
#     # return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info)
#     return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info) #new

# @app.route("/user_search")
# def search_user():
#     search_word = request.args.get("search")
#     key = request.args.get("key")
#     if not search_word or not key:
#         return "Please provide search word and key"
#     if key == "name":
#         results = ParkingLot.query.filter(ParkingLot.name.ilike(f"%{search_word}%")).all()
   
#     else:
#         results = ParkingLot.query.filter(ParkingLot.pincode.ilike(f"%{search_word}%")).all()
#     return render_template("user_result.html",results = results,key = key)

# @app.route("/user_dashboard")
# def user_dashboard():
#     user_id = session.get("user_id")
#     if not user_id:
#         return redirect("/")
#     this_user = User.query.get(user_id)
#     if not this_user:
#         return redirect("/")
#     parkinglots = ParkingLot.query.all() 

#     lot_info = []
#     for lot in parkinglots:
#         total_spots = lot.maximum_spot
#         booked_spots = Booking.query.filter_by(lot_id = lot.id,release_time = None).count() #new


#         available_spots = total_spots - booked_spots
#         lot_info.append({
#             "id":lot.id,
#             "name":lot.name,
#             "address":lot.address,
#             "available":available_spots,
#             "total":total_spots
#         })
    
#     active_spots = Booking.query.filter_by(user_id = this_user.id).all()
    
#     return render_template("user_dashboard.html",this_user = this_user,spots = active_spots,lot_info = lot_info)


# @app.route("/release/<int:booking_id>" ,methods = ["GET","POST"])
# def release(booking_id):

#     booking = Booking.query.get(booking_id)
   
#     if not booking:
#         return "Booking not found"
#     ist = pytz.timezone('Asia/Kolkata')
#     current_time = datetime.now(ist)
#     parking_time = booking.parking_time
#     if parking_time.tzinfo is None:
#         parking_time = ist.localize(parking_time)
    
#     duration = (current_time - parking_time).total_seconds()/3600
#     hours = math.ceil(duration)
   
#     lot = ParkingLot.query.get(booking.lot_id)
#     cost = round(hours * lot.price_per_hour,2)

#     if request.method == "GET":
      
#         return render_template("release.html",booking = booking,cost = cost,current_time = current_time)
#     else:
       
#         booking.release_time = current_time
#         booking.total_cost = cost
#         booking.available = True #new

#         db.session.commit()
#         return redirect("/user_dashboard")
 
   
# @app.route("/admin_summary")
# def admin_summary():
#     lots = ParkingLot.query.all()
#     lot_names = []
#     lot_revenues = []
#     total_available = 0
#     total_occupied = 0
#     for lot in lots:
#         bookings = Booking.query.filter_by(lot_id = lot.id).all()
#         revenue = sum(int(b.total_cost or 0) for b in bookings)
#         lot_names.append(lot.name)
#         lot_revenues.append(revenue)
#         occupied = len(bookings)
#         available = lot.maximum_spot - occupied
#         total_occupied += occupied
#         total_available += available
#     static_path = os.path.join(os.getcwd(), "static")
#     plt.figure(figsize=(9, 6))
#     plt.bar(lot_names, lot_revenues ,color = "skyblue")
#     plt.xlabel("Parking Lots")
#     plt.ylabel("Revenue")
#     plt.title("Revenue from each Parking Lot")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.savefig(os.path.join(static_path,"admin_summary.png"))
#     plt.clf()

#     labels = ["Availables Spot","Occupied Spots"]
#     values = [total_available,total_occupied]
#     colors = ["#4e73df", "#1cc88a"]
#     plt.figure()
#     plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
#     plt.title("Summary of available and occupied Spots")
#     plt.savefig(os.path.join(static_path,"admin_summary_bar.png"))
#     plt.clf()
#     pl = len(lots)
#     bk = Booking.query.count()
#     us = User.query.count()
#     total_cost = sum(lot_revenues)
#     return render_template("admin_summary.html",pl = pl,bk = bk,us = us,total_cost = total_cost)

# @app.route("/user_summary")
# def user_summary():
#     user_id = session.get("user_id")
#     if not user_id:
#         return redirect("/")
#     user = User.query.get(user_id)
#     bookings = Booking.query.filter_by(user_id = user.id).all()
#     lot_names = [ParkingLot.query.get(b.lot_id).name for b in bookings]
#     lot_counts = Counter(lot_names)
     
#     plt.figure(figsize=(9, 6))
#     plt.bar(lot_counts.keys(), lot_counts.values(),color = "skyblue")
#     plt.xlabel("Parking Lot")
#     plt.ylabel("No. of times used")
#     plt.title("Your Used Parking Spot")
#     plt.tight_layout()
#     graph_path = os.path.join("static", "user_usage_summary.png")
#     plt.savefig(graph_path)
#     plt.clf

#     return render_template("user_summary.html",user = user,bookings = bookings,lot_counts = lot_counts,graph_path = graph_path)



from flask import Flask,render_template,redirect,request,session
import math
import pytz
from flask import current_app as app #if we do directly import then it will lead to circular flow
#current _app refers to app object tsht we created
from .models import *
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

# @app.route("/",methods = ["GET","POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form.get("password")
#         this_user = User.query.filter_by(username = username).first() #lhs >> table,rhs>>form data
#         parkinglots = ParkingLot.query.all()
#         if this_user:
#             if this_user.password  == password:
#                 if this_user.type == "admin":
#                     lot_info = []
#                     for lot in parkinglots:
#                         total_spots = lot.maximum_spot
#                         booked = Booking.query.filter_by(lot_id = lot.id).count()
#                         available = total_spots - booked
#                         lot_info.append({"id":lot.id,"name":lot.name,"address":lot.address,"available":available,"total":total_spots})
#                     return render_template("admin_dashboard.html",this_user = this_user,parkinglots = parkinglots,lot_info = lot_info)
#                 else:
#                     spots = Booking.query.filter_by(user_id = this_user.id).all()
#                     lot_info = []
#                     for lot in parkinglots:
#                         total_spots = lot.maximum_spot
#                         booked = Booking.query.filter_by(lot_id = lot.id).count()
#                         available = total_spots - booked
#                         lot_info.append({"id":lot.id,"name":lot.name,"address":lot.address,"available":available,"total":total_spots})
#                     return render_template("user_dashboard.html",this_user = this_user,spots = spots,lot_info = lot_info)
#             else:
#                 return "Password is wrong"
#         else:
#             return "user does not Exist"
        
#     return render_template("login.html")

@app.route("/",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form.get("password")
        this_user = User.query.filter_by(username = username).first() #lhs >> table,rhs>>form data
        parkinglots = ParkingLot.query.all()
        if this_user:
            if this_user.password  == password:
                session["user_id"] = this_user.id
                if this_user.type == "admin":
                    lot_info = []
                    for lot in parkinglots:
                        total_spots = lot.maximum_spot
                        booked = Booking.query.filter_by(lot_id = lot.id).count()
                        available = total_spots - booked
                        lot_info.append({"id":lot.id,"name":lot.name,"address":lot.address,"available":available,"total":total_spots})
                    return render_template("admin_dashboard.html",this_user = this_user,parkinglots = parkinglots,lot_info = lot_info)
                else:
                    spots = Booking.query.filter_by(user_id = this_user.id).all()
                    lot_info = []
                    for lot in parkinglots:
                        total_spots = lot.maximum_spot
                        booked = Booking.query.filter_by(lot_id = lot.id).count()
                        available = total_spots - booked
                        lot_info.append({"id":lot.id,"name":lot.name,"address":lot.address,"available":available,"total":total_spots})
                    return render_template("user_dashboard.html",this_user = this_user,spots = spots,lot_info = lot_info)
            else:
                return "Password is wrong"
        else:
            return "user does not Exist"
        
    return render_template("login.html")




@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form.get("password")
        user_name = User.query.filter_by(username = username).first()
        user_email = User.query.filter_by(email = email).first()
        if user_name or user_email:
           return "user already exist"
        else:
            user = User(username = username,email = email,password = password)
            db.session.add(user)
            
            db.session.commit()
            return redirect("/")
    return render_template("register.html")

@app.route("/users")
def user():
    users = User.query.filter_by(type = "general").all()
    return render_template("user.html",users = users)



@app.route("/add_parkinglot",methods = ["GET","POST"])
def create_parkinglot():

    # new
    # user_id = session.get("user_id")
    # this_user = User.query.get(user_id)
    # if not this_user or this_user.type != "admin":
    #     return redirect("/")

    # new

    this_user = User.query.filter_by(type = "admin").first()
    parkinglots = ParkingLot.query.all()
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        pincode = request.form["pincode"]
        price_per_hour = request.form["price_per_hour"]
        maximum_spot = int(request.form["maximum_spot"])

        existing_parkinglot = ParkingLot.query.filter_by(name = name).first()
        if existing_parkinglot:
            return "parkinglot already exist"
        parkinglot = ParkingLot(name = name,address = address,pincode = pincode,price_per_hour = price_per_hour,maximum_spot = maximum_spot,user_id = this_user.id)
        db.session.add(parkinglot)
        db.session.commit()

        parkinglots = ParkingLot.query.all()
        lot_info = []
        for lot in parkinglots:
            total_spots = lot.maximum_spot
            booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
            available_spots = total_spots - booked_spots
            lot_info.append({
                "id":lot.id,
                "name":lot.name,
                "address":lot.address,
                "available":available_spots,
                "total":total_spots
            })
        return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info)
    return render_template("add_parkinglot.html",this_user = this_user,parkinglots = parkinglots)
    
# @app.route("/delete_parkinglot/<int:parkinglot_id>",methods = ["GET","POST"])
# def delete_parkinglot(parkinglot_id):
#     this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
#     bookings = Booking.query.filter_by(lot_id=this_parkinglot.id,available = False).all()
#     if bookings:
#         return "cannot delete this parkinglot because it has bookings"
#     ParkingLot.query.filter_by(id = parkinglot_id).delete()
#     db.session.delete(this_parkinglot)
#     db.session.commit()
#     this_user = User.query.filter_by(type = "admin").first()
#     parkinglots = ParkingLot.query.all()

#     lot_info = []
#     for lot in parkinglots:
#         total_spots = lot.maximum_spot
#         booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
#         available_spots = total_spots - booked_spots
#         lot_info.append({
#             "id":lot.id,
#             "name":lot.name,
#             "address":lot.address,
#             "available":available_spots,
#             "total":total_spots
#         })
#     return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info,parkinglots = parkinglots)
    
   
@app.route("/delete_parkinglot/<int:parkinglot_id>",methods = ["GET","POST"])
def delete_parkinglot(parkinglot_id):
    this_parkinglot = ParkingLot.query.get(parkinglot_id)
    if not this_parkinglot:
        return "parkinglot not found",404
    bookings = Booking.query.filter_by(lot_id=this_parkinglot.id,available = False).all()
    if bookings:
        return "<h1>cannot delete this parkinglot because it has bookings</h1>"
    ParkingLot.query.filter_by(id = parkinglot_id).delete()
    db.session.delete(this_parkinglot)
    db.session.commit()
    this_user = User.query.filter_by(type = "admin").first()
    parkinglots = ParkingLot.query.all()

    lot_info = []
    for lot in parkinglots:
        total_spots = lot.maximum_spot
        booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
        available_spots = total_spots - booked_spots
        lot_info.append({
            "id":lot.id,
            "name":lot.name,
            "address":lot.address,
            "available":available_spots,
            "total":total_spots
        })
    return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info,parkinglots = parkinglots)



@app.route("/edit_parkinglot/<int:parkinglot_id>",methods = ["GET","POST"])
def edit_parkinglot(parkinglot_id):
    this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
    print(this_parkinglot)
    if request.method == "POST":
        this_parkinglot.name = request.form["name"]
        this_parkinglot.address = request.form["address"]
        this_parkinglot.pincode = request.form["pincode"]
        this_parkinglot.price_per_hour = request.form["price_per_hour"]
        this_parkinglot.maximum_spot = request.form["maximum_spot"]
        db.session.commit()
        this_user = User.query.filter_by(type = "admin").first()
        parkinglots = ParkingLot.query.all()
        
        lot_info = []
        for lot in parkinglots:
            total_spots = lot.maximum_spot
            booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
            available_spots = total_spots - booked_spots
            lot_info.append({
                "id":lot.id,
                "name":lot.name,
                "address":lot.address,
                "available":available_spots,
                "total":total_spots
            })
        return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info)
    return render_template("edit_parkinglot.html",this_parkinglot = this_parkinglot)


@app.route("/view_lot/<int:parkinglot_id>",methods = ["GET","POST"])  
def view_parkinglot(parkinglot_id):
    
    this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
    bookings = Booking.query.filter_by(lot_id = this_parkinglot.id,release_time = None).all()
    booking_by_spot = {booking.spot_id:booking for booking in bookings}
    booked_spots_ids = list(booking_by_spot.keys())
    return render_template("view_lot.html",this_parkinglot = this_parkinglot,booked_spots_ids = booked_spots_ids,bookings_by_spot = booking_by_spot)


@app.route("/delete_spot/<int:parkinglot_id>/<int:spot_id>",methods = ["GET","POST"])
def delete_spot(parkinglot_id,spot_id):
    booking = Booking.query.filter_by(lot_id = parkinglot_id,spot_id = spot_id).first()
    if booking:
        return "cannot delete this spot because it has booking"
    spot = Booking.query.filter_by(id = spot_id).first()
    db.session.delete(spot)
    db.session.commit()
    return f"Spot {spot_id} deleted successfully"





# @app.route("/book/<int:parkinglot_id>/<int:user_id>",methods = ["GET","POST"])
# def book(parkinglot_id,user_id):
#     this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
#     this_user = User.query.filter_by(id = user_id).first()
#     spots = Booking.query.filter_by(lot_id = this_parkinglot.id).all()
#     if request.method == "GET":
#         existing_spots = Booking.query.filter_by(lot_id = this_parkinglot.id).count()
#         next_spot_id = existing_spots + 1
#         if next_spot_id > this_parkinglot.maximum_spot:
#             return render_template("sorry all full")
#         return render_template("book.html",this_parkinglot = this_parkinglot,this_user = this_user,next_spot_id = next_spot_id)
#     else:
#         vehicle_no = request.form["vehicle_no"]
#         spot_id = int(request.form["spot_id"])
#         lot_id = int(request.form["lot_id"])
#         user_id = int(request.form["user_id"])
#         booking = Booking(vehicle_no = vehicle_no,spot_id = spot_id,lot_id = lot_id,user_id = user_id)
#         db.session.add(booking)
#         db.session.commit()
#         spots = Booking.query.filter_by(user_id = this_user.id).all()
#         parkinglots = ParkingLot.query.all()
#         lot_info = []
#         for lot in parkinglots:
#             total_spots = lot.maximum_spot
#             booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
#             available_spots = total_spots - booked_spots
#             lot_info.append({
#                 "id":lot.id,
#                 "name":lot.name,
#                 "address":lot.address,
#                 "available":available_spots,
#                 "total":total_spots
#             })
#         history = Booking.query.filter(Booking.user_id == this_user.id,Booking.release_time != None).all()  #new
#         return render_template("user_dashboard.html",this_user = this_user,spots = spots,lot_info = lot_info)
       
# new

@app.route("/book/<int:parkinglot_id>/<int:user_id>",methods = ["GET","POST"])
def book(parkinglot_id,user_id):
    this_parkinglot = ParkingLot.query.filter_by(id = parkinglot_id).first()
    this_user = User.query.filter_by(id = user_id).first()
    spots = Booking.query.filter_by(lot_id = this_parkinglot.id).all()
    if request.method == "GET":
        existing_spots = Booking.query.filter_by(lot_id = this_parkinglot.id).count()
        next_spot_id = existing_spots + 1
        if next_spot_id > this_parkinglot.maximum_spot:
            return render_template("sorry all full")
        return render_template("book.html",this_parkinglot = this_parkinglot,this_user = this_user,next_spot_id = next_spot_id)
    else:
        vehicle_no = request.form["vehicle_no"]
        spot_id = int(request.form["spot_id"])
        lot_id = int(request.form["lot_id"])
        user_id = int(request.form["user_id"])

        existing_booking = Booking.query.filter_by(vehicle_no = vehicle_no,available = False).first()

        if existing_booking:
            
                return "vehicle_already_booked.html"
           
        booking = Booking(vehicle_no = vehicle_no,spot_id = spot_id,lot_id = lot_id,user_id = user_id,parking_time = datetime.now(),available = False)
        # booking = Booking(vehicle_no = vehicle_no,spot_id = spot_id,lot_id = lot_id,user_id = user_id)
        db.session.add(booking)
        db.session.commit()
        spots = Booking.query.filter_by(user_id = this_user.id).all()
        parkinglots = ParkingLot.query.all()
        lot_info = []
        for lot in parkinglots:
            total_spots = lot.maximum_spot
            booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
            available_spots = total_spots - booked_spots
            lot_info.append({
                "id":lot.id,
                "name":lot.name,
                "address":lot.address,
                "available":available_spots,
                "total":total_spots
            })
        history = Booking.query.filter(Booking.user_id == this_user.id,Booking.release_time != None).all()  #new
        return render_template("user_dashboard.html",this_user = this_user,spots = spots,lot_info = lot_info)
       

      


# new

@app.route("/view_spot/<int:parkinglot_id>/<int:spot_id>")
def view_spots(parkinglot_id,spot_id):
    lot = ParkingLot.query.get(parkinglot_id)
    spot = Booking.query.filter_by(lot_id = lot.id,spot_id = spot_id).first()
    if not spot or not lot:
        return "<h1>Spot is not booked</h1>"
    user = User.query.get(spot.user_id)
    return render_template("single_view_spot.html",spot = spot,lot = lot,user = user)



    
@app.route("/search")
def search():
    search_word = request.args.get("search")
    key = request.args.get("key")
    if not search_word or not key:
        return "Please provide search word and key"
    if key == "name":
        results = ParkingLot.query.filter(ParkingLot.name.ilike(f"%{search_word}%")).all()
   
    else:
        results = ParkingLot.query.filter(ParkingLot.pincode.ilike(f"%{search_word}%")).all()
    return render_template("result.html",results = results,key = key)


@app.route("/admin_dashboard")
def admin_dashboard():
    this_user = User.query.filter_by(type = "admin").first()
    # user_id = session.get("user_id") #new
    # this_user = User.query.get(user_id) #new

    parkinglots = ParkingLot.query.all() 

    lot_info = []
    for lot in parkinglots:
        total_spots = lot.maximum_spot
        # booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
        booked_spots = Booking.query.filter_by(lot_id = lot.id,release_time = None).count()  #new
        available_spots = total_spots - booked_spots
        lot_info.append({
            "id":lot.id,
            "name":lot.name,
            "address":lot.address,
            "available":available_spots,
            "total":total_spots
        })
    return render_template("admin_dashboard.html",this_user = this_user,lot_info = lot_info)

@app.route("/user_search")
def search_user():
    search_word = request.args.get("search")
    key = request.args.get("key")
    if not search_word or not key:
        return "Please provide search word and key"
    if key == "name":
        results = ParkingLot.query.filter(ParkingLot.name.ilike(f"%{search_word}%")).all()
   
    else:
        results = ParkingLot.query.filter(ParkingLot.pincode.ilike(f"%{search_word}%")).all()
    return render_template("user_result.html",results = results,key = key)

# @app.route("/user_dashboard")
# def user_dashboard():
#     this_user = User.query.filter_by(type = "general").first()
#     parkinglots = ParkingLot.query.all() 

#     lot_info = []
#     for lot in parkinglots:
#         total_spots = lot.maximum_spot
#         booked_spots = Booking.query.filter_by(lot_id = lot.id).count()
#         available_spots = total_spots - booked_spots
#         lot_info.append({
#             "id":lot.id,
#             "name":lot.name,
#             "address":lot.address,
#             "available":available_spots,
#             "total":total_spots
#         })
#         spots = Booking.query.filter_by(user_id = this_user.id).all()
#         lot_info = []
#         for lot in parkinglots:
#             total_spots = lot.maximum_spot
#             booked = Booking.query.filter_by(lot_id = lot.id).count()
#             available = total_spots - booked
#             lot_info.append({"id":lot.id,"name":lot.name,"address":lot.address,"available":available,"total":total_spots})
#         return render_template("user_dashboard.html",this_user = this_user,spots = spots,lot_info = lot_info)
#     return render_template("user_dashboard.html",this_user = this_user,lot_info = lot_info)


# new

@app.route("/user_dashboard")
def user_dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")
    this_user = User.query.get(user_id)
    if not this_user:
        return redirect("/")
    parkinglots = ParkingLot.query.all() 

    lot_info = []
    for lot in parkinglots:
        total_spots = lot.maximum_spot
        # booked_spots = Booking.query.filter_by(lot_id = lot.id).count()

        booked_spots = Booking.query.filter_by(lot_id = lot.id,release_time = None).count() #new


        available_spots = total_spots - booked_spots
        lot_info.append({
            "id":lot.id,
            "name":lot.name,
            "address":lot.address,
            "available":available_spots,
            "total":total_spots
        })
    # active_spots = Booking.query.filter_by(user_id = this_user.id,release_time= None).all()
    active_spots = Booking.query.filter_by(user_id = this_user.id).all()  #new
    
    return render_template("user_dashboard.html",this_user = this_user,spots = active_spots,lot_info = lot_info)

# new


# @app.route("/release/<int:spot_id>" ,methods = ["GET","POST"])
# def release(spot_id):
   
#     booking = Booking.query.filter_by(spot_id = spot_id).first()
#     if request.method == "GET":
#         return render_template("release.html",spot_id=spot_id,booking = booking)
#     else:
#         return "Spot released"

# new
@app.route("/release/<int:booking_id>" ,methods = ["GET","POST"])
def release(booking_id):

    booking = Booking.query.get(booking_id)
   
    if not booking:
        return "Booking not found"
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    parking_time = booking.parking_time
    if parking_time.tzinfo is None:
        parking_time = ist.localize(parking_time)
    
    duration = (current_time - parking_time).total_seconds()/3600
    hours = math.ceil(duration)
   
    lot = ParkingLot.query.get(booking.lot_id)
    cost = round(hours * lot.price_per_hour,2)

    if request.method == "GET":
      
        return render_template("release.html",booking = booking,cost = cost,current_time = current_time)
    else:
       
        booking.release_time = current_time
        booking.total_cost = cost
        booking.available = True #new
        db.session.commit()
        print("Booking released for spot:", booking.spot_id)
        print("Available status now:", booking.available)
        return redirect("/user_dashboard")
       
    
        
    
# new

# @app.route("/admin_summary")
# def admin_summary():
#     pl = len(ParkingLot.query.all())
#     bk = len(Booking.query.all())
#     cost = sum(int(booking.total_cost or 0) for booking in Booking.query.all())
#     labels = ["Parking Lots","Bookings","Total Cost"]
#     sizes = [pl,bk,cost]
#     colors = ["#4e73df", "#1cc88a", "#36b9cc"]
#     plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
#     plt.title("Summary of Parking Lots")
#     # plt.axis("equal")
#     plt.savefig("static/admin_summary.png")
#     plt.clf()

#     labels = ["Total Parking Lots","Total Bookings","Total Cost"]
#     sizes = [pl,bk,cost]
#     plt.bar(labels, sizes)
#     plt.xlabel("Parking Lots")
#     plt.ylabel("Cost")
#     plt.title("Summary of Parking Lots")
#     plt.savefig("static/admin_summary_bar.png")
#     plt.clf()

#     us = len(User.query.all())  


#     return render_template("admin_summary.html",pl = pl,bk = bk,us = us)

   
@app.route("/admin_summary")
def admin_summary():
    lots = ParkingLot.query.all()
    lot_names = []
    lot_revenues = []
    total_available = 0
    total_occupied = 0
    for lot in lots:
        booking = Booking.query.filter_by(lot_id = lot.id,release_time = None).all() #added on 24
        bookings = Booking.query.filter_by(lot_id = lot.id).all()

        revenue = sum(int(b.total_cost or 0) for b in bookings)
        lot_names.append(lot.name)
        lot_revenues.append(revenue)
        occupied = len(booking)   #bookings >> booking on 24
        available = lot.maximum_spot - occupied
        total_occupied += occupied
        total_available += available
    static_path = os.path.join(os.getcwd(), "static")
    plt.figure(figsize=(9, 6))
    plt.bar(lot_names, lot_revenues ,color = "skyblue")
    plt.xlabel("Parking Lots")
    plt.ylabel("Revenue")
    plt.title("Revenue from each Parking Lot")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(static_path,"admin_summary.png"))
    plt.clf()

    labels = ["Availables Spot","Occupied Spots"]
    values = [total_available,total_occupied]
    colors = ["#4e73df", "#1cc88a"]
    plt.figure()
    if sum(values) == 0:
        plt.text(0.5, 0.5, "No Spots Booked", fontsize=20, ha="center", va="center",fontweight="bold")
        plt.axis("off")
    else:

        plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title("Summary of available and occupied Spots")
    plt.savefig(os.path.join(static_path,"admin_summary_bar.png"))
    plt.clf()
    pl = len(lots)
    bk = Booking.query.count()
    us = User.query.count()
    total_cost = sum(lot_revenues)
    return render_template("admin_summary.html",pl = pl,bk = bk,us = us,total_cost = total_cost)

@app.route("/user_summary")
def user_summary():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")
    user = User.query.get(user_id)
    bookings = Booking.query.filter_by(user_id = user.id).all()
    lot_names = [ParkingLot.query.get(b.lot_id).name for b in bookings]
    lot_counts = Counter(lot_names)
     
    plt.figure(figsize=(9, 6))
    plt.bar(lot_counts.keys(), lot_counts.values(),color = "skyblue")
    plt.xlabel("Parking Lot")
    plt.ylabel("No. of times used")
    plt.title("Your Used Parking Spot")
    plt.tight_layout()
    graph_path = os.path.join("static", "user_usage_summary.png")
    plt.savefig(graph_path)
    plt.clf

    return render_template("user_summary.html",user = user,bookings = bookings,lot_counts = lot_counts,graph_path = graph_path)

