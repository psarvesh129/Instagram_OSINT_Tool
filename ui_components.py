import tkinter as tk
from tkinter import messagebox, ttk
from helpers import show_result, run_with_proxychains, get_random_user_agent
from insta_loader import InstaLoaderWrapper

def create_login_widgets(app, frame):
    app.canvas = tk.Canvas(frame, width=1200, height=800)
    app.canvas.pack(fill=tk.BOTH, expand=True)
    app.logo_image = tk.PhotoImage(file="./logo.png")
    app.canvas.create_image(600, 200, image=app.logo_image)

    app.username_label = ttk.Label(frame, text="Instagram Username:")
    app.username_entry = ttk.Entry(frame)

    app.password_label = ttk.Label(frame, text="Instagram Password:")
    app.password_entry = ttk.Entry(frame, show="*")

    app.login_button = ttk.Button(frame, text="Login", command=lambda: login_instaloader(app))

    app.canvas.create_window(600, 350, window=app.username_label)
    app.canvas.create_window(600, 380, window=app.username_entry, width=200)
    app.canvas.create_window(600, 410, window=app.password_label)
    app.canvas.create_window(600, 440, window=app.password_entry, width=200)
    app.canvas.create_window(600, 470, window=app.login_button)

def create_profile_widgets(app, frame):
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)

    app.target_label = ttk.Label(frame, text="Target Username:")
    app.target_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    app.target_entry = ttk.Entry(frame)
    app.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

    app.find_button = ttk.Button(frame, text="Find Profile", command=lambda: get_profile_data(app))
    app.find_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

    app.profile_info_tree = ttk.Treeview(frame, columns=("Attribute", "Value"), show='headings')
    app.profile_info_tree.heading("Attribute", text="Attribute")
    app.profile_info_tree.heading("Value", text="Value")
    app.profile_info_tree.column("Attribute", width=150)
    app.profile_info_tree.column("Value", width=600)
    app.profile_info_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

    app.scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=app.profile_info_tree.yview)
    app.profile_info_tree.configure(yscrollcommand=app.scrollbar_y.set)
    app.scrollbar_y.grid(row=2, column=2, sticky=tk.NS)

def create_actions_widgets(app, frame):
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(9, weight=1)

    app.download_profile_button = ttk.Button(frame, text="Download Full Profile", command=lambda: download_full_profile(app))
    app.download_profile_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)

    app.download_comments_button = ttk.Button(frame, text="Download All Comments", command=lambda: download_comments(app))
    app.download_comments_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)

    app.get_followers_button = ttk.Button(frame, text="Get List of Followers", command=lambda: display_followers(app))
    app.get_followers_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)

    app.get_following_button = ttk.Button(frame, text="Get List of Following", command=lambda: display_following(app))
    app.get_following_button.grid(row=3, column=0, padx=5, pady=5, sticky=tk.EW)

    app.get_likes_button = ttk.Button(frame, text="Total Likes", command=lambda: display_likes(app))
    app.get_likes_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.EW)

    app.get_post_insights_button = ttk.Button(frame, text="Get Post Insights", command=lambda: get_post_insights(app))
    app.get_post_insights_button.grid(row=5, column=0, padx=5, pady=5, sticky=tk.EW)

    app.get_tagged_users_button = ttk.Button(frame, text="List of Users Tagged by Target", command=lambda: display_tagged_users(app))
    app.get_tagged_users_button.grid(row=6, column=0, padx=5, pady=5, sticky=tk.EW)

    app.get_users_tagged_target_button = ttk.Button(frame, text="List of Users Who Tagged Target", command=lambda: display_users_tagged_target(app))
    app.get_users_tagged_target_button.grid(row=7, column=0, padx=5, pady=5, sticky=tk.EW)

    app.result_text = tk.Text(frame, wrap='none')
    app.result_text.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

    app.scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=app.result_text.yview)
    app.scrollbar_y.grid(row=8, column=2, sticky=tk.NS)
    app.result_text.configure(yscrollcommand=app.scrollbar_y.set)

    app.scrollbar_x = ttk.Scrollbar(frame, orient='horizontal', command=app.result_text.xview)
    app.scrollbar_x.grid(row=9, column=0, columnspan=2, sticky=tk.EW)
    app.result_text.configure(xscrollcommand=app.scrollbar_x.set)

def login_instaloader(app):
    username = app.username_entry.get()
    password = app.password_entry.get()
    try:
        app.L = InstaLoaderWrapper()
        message = app.L.login(username, password)
        messagebox.showinfo("Login Status", message)
    except Exception as e:
        messagebox.showerror("Login Error", str(e))

def get_profile_data(app):
    try:
        target_username = app.target_entry.get()
        app.profile = app.L.get_profile(target_username)
        messagebox.showinfo("Profile Status", f"Profile '{target_username}' found")
        display_info(app)
    except Exception as e:
        messagebox.showerror("Profile Error", str(e))

def display_info(app):
    try:
        profile_info = [
            ("Username", app.profile.username),
            ("Profile Name", app.profile.full_name),
            ("URL", f"https://www.instagram.com/{app.profile.username}/"),
            ("Followers", app.profile.followers),
            ("Following", app.profile.followees),
            ("Number of Posts", app.profile.mediacount),
            ("Bio", app.profile.biography),
            ("Profile Picture URL", app.profile.profile_pic_url),
            ("Is Business Account?", app.profile.is_business_account),
            ("External URL", app.profile.external_url if hasattr(app.profile, 'external_url') else "N/A"),
            ("Joined Recently?", app.profile.is_joined_recently if hasattr(app.profile, 'is_joined_recently') else "N/A"),
            ("Business Category Name", app.profile.business_category_name if hasattr(app.profile, 'business_category_name') else "N/A"),
            ("Is private?", app.profile.is_private),
            ("Is Verified?", app.profile.is_verified)
        ]
        app.profile_info_tree.delete(*app.profile_info_tree.get_children())
        for item in profile_info:
            app.profile_info_tree.insert('', 'end', values=item)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def download_full_profile(app):
    try:
        target_username = app.target_entry.get()
        run_with_proxychains(f"instaloader --login={app.username_entry.get()} --password={app.password_entry.get()} {target_username}")
        messagebox.showinfo("Download Full Profile", f"Full profile of {target_username} has been downloaded.")
    except Exception as e:
        messagebox.showerror("Download Error", str(e))

def download_comments(app):
    try:
        comments = []
        for post in app.profile.get_posts():
            for comment in post.get_comments():
                if hasattr(comment.owner, 'username'):
                    comments.append([post.mediaid, comment.owner.username, comment.text])
        if not comments:
            comments.append(["No data available", "", ""])
        show_result(app, comments, ["Media ID", "Commenter Username", "Comment"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve comments: {str(e)}")

def display_followers(app):
    try:
        followers = []
        for follower in app.profile.get_followers():
            followers.append([follower.userid, follower.username, follower.full_name])
        if not followers:
            followers.append(["No data available", "", ""])
        show_result(app, followers, ["ID", "Username", "Full Name"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve followers: {str(e)}")

def display_following(app):
    try:
        followees = []
        for followee in app.profile.get_followees():
            followees.append([followee.userid, followee.username, followee.full_name])
        if not followees:
            followees.append(["No data available", "", ""])
        show_result(app, followees, ["ID", "Username", "Full Name"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve following: {str(e)}")

def display_likes(app):
    try:
        total_likes = sum([post.likes for post in app.profile.get_posts()])
        if total_likes == 0:
            show_result(app, [["Total Likes", "No data available"]], ["Metric", "Value"])
        else:
            show_result(app, [["Total Likes", total_likes]], ["Metric", "Value"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve likes: {str(e)}")

def get_post_insights(app):
    try:
        post_insights = []
        for post in app.profile.get_posts():
            post_info = {
                "Post ID": post.mediaid,
                "Caption": post.caption,
                "Likes": post.likes,
                "Comments": post.comments,
                "Date Posted": post.date_utc,
                "URL": f"https://www.instagram.com/p/{post.shortcode}/",
                "Comments Details": [(comment.owner.username, comment.text) for comment in post.get_comments() if hasattr(comment.owner, 'username')]
            }
            post_insights.append(post_info)
        if not post_insights:
            post_insights.append({"Post ID": "No data available", "Caption": "", "Likes": "", "Comments": "", "Date Posted": "", "URL": "", "Comments Details": ""})
        show_post_insights(app, post_insights)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve post insights: {str(e)}")

def display_tagged_users(app):
    try:
        tagged_users = []
        for post in app.profile.get_posts():
            for user in post.tagged_users:
                if hasattr(user, 'username'):
                    tagged_users.append([post.mediaid, user.username])
        if not tagged_users:
            tagged_users.append(["No data available", ""])
        show_result(app, tagged_users, ["Media ID", "Tagged Username"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve tagged users: {str(e)}")

def display_users_tagged_target(app):
    try:
        tagged_by_others = []
        for post in app.profile.get_tagged_posts():
            if hasattr(post.owner_profile, 'username'):
                tagged_by_others.append([post.mediaid, post.owner_profile.username])
        if not tagged_by_others:
            tagged_by_others.append(["No data available", ""])
        show_result(app, tagged_by_others, ["Media ID", "Tagger Username"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve users who tagged the target: {str(e)}")

def show_post_insights(app, post_insights):
    try:
        app.result_text.delete(1.0, tk.END)
        for post_info in post_insights:
            app.result_text.insert(tk.END, f"Post ID: {post_info['Post ID']}\n")
            app.result_text.insert(tk.END, f"Caption: {post_info['Caption']}\n")
            app.result_text.insert(tk.END, f"Likes: {post_info['Likes']}\n")
            app.result_text.insert(tk.END, f"Comments: {post_info['Comments']}\n")
            app.result_text.insert(tk.END, f"Date Posted: {post_info['Date Posted']}\n")
            app.result_text.insert(tk.END, f"URL: {post_info['URL']}\n")
            app.result_text.insert(tk.END, "Comments Details:\n")
            for comment in post_info['Comments Details']:
                app.result_text.insert(tk.END, f"\tUser: {comment[0]}, Comment: {comment[1]}\n")
            app.result_text.insert(tk.END, "-"*50 + "\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# GPCSSI2024CW407