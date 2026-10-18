import json
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash
from app.core.config import settings
from app.models.user import User
from app.models.profile import Profile
from app.models.skill import SkillCategory, Skill
from app.models.experience import Experience
from app.models.project import Project
from app.models.dashboard_layout import DashboardLayout
from app.models.attendance import GeofenceZone

def seed_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if already seeded
        admin_exists = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if admin_exists:
            print("Database already seeded with admin user. Skipping.")
            return

        print("Seeding administrator user...")
        admin = User(
            name="Shashidhar P C",
            email=settings.ADMIN_EMAIL,
            password_hash=get_password_hash(settings.ADMIN_PASSWORD),
            role="ADMIN"
        )
        db.add(admin)
        db.flush()

        # Seed Dashboard Layout
        layout = DashboardLayout(
            user_id=admin.id,
            widgets_config="""[
                {"id":"stats","colSpan":12,"isVisible":true,"order":0},
                {"id":"quick_actions","colSpan":4,"isVisible":true,"order":1},
                {"id":"projects","colSpan":8,"isVisible":true,"order":2},
                {"id":"messages","colSpan":6,"isVisible":true,"order":3},
                {"id":"skills","colSpan":6,"isVisible":true,"order":4},
                {"id":"activity","colSpan":8,"isVisible":true,"order":5},
                {"id":"appearance","colSpan":4,"isVisible":true,"order":6}
            ]""",
            accent_gradient="violet-blue",
            font_size="default",
            motion_enabled=True
        )
        db.add(layout)

        # Seed Profile
        profile = Profile(
            id="default",
            full_name="Shashidhar P C",
            title="Full Stack Software Engineer",
            headline="Developing secure, database-driven web applications using Python, Flask, JavaScript, and PHP. Skilled in architecting REST APIs, implementing Role-Based Access Control, and designing scalable MySQL & MongoDB schemas.",
            bio="Full Stack Software Engineer based in Bengaluru with a strong foundation in Data Structures, Algorithms, Object Oriented Design, and the full Software Development Life Cycle (SDLC). Experienced in developing secure, multi-tier web platforms with Python, Flask, PHP, JavaScript, and modern database architectures. Master of Computer Applications (MCA) graduate from Presidency College (8.75 CGPA) and BCA graduate from Sahyadri Science College (89.86%). Proven track record through production web application development, including automated QR code & geofencing attendance architectures and multi-tier vehicle rental systems.",
            location="Bengaluru, Karnataka, India",
            available_for_hire=True,
            social_links=json.dumps({
                "github": "https://github.com/shashidharpc",
                "linkedin": "https://linkedin.com/in/shashidharpc",
                "email": "shashidharpc10@gmail.com"
            })
        )
        db.add(profile)

        # Seed Skills Categories
        cat_lang = SkillCategory(name="Languages & Core Stack", description="Primary programming languages and web fundamentals", order=1)
        cat_backend = SkillCategory(name="Frameworks & Backend Architecture", description="APIs, application servers, and microservices", order=2)
        cat_db = SkillCategory(name="Databases & Cloud Infrastructure", description="Relational and document storage solutions", order=3)
        cat_arch = SkillCategory(name="Software Engineering & Tools", description="Design methodologies, version control, and testing", order=4)
        db.add_all([cat_lang, cat_backend, cat_db, cat_arch])
        db.flush()

        # Seed individual skills
        skills_data = [
            # Languages
            ("Python", 95, True, 1, cat_lang.id),
            ("JavaScript", 92, True, 2, cat_lang.id),
            ("PHP", 88, True, 3, cat_lang.id),
            ("SQL", 90, True, 4, cat_lang.id),
            ("Java", 80, False, 5, cat_lang.id),
            ("C", 78, False, 6, cat_lang.id),
            ("HTML5 & CSS3", 94, False, 7, cat_lang.id),
            # Backend
            ("Flask", 92, True, 1, cat_backend.id),
            ("FastAPI", 90, True, 2, cat_backend.id),
            ("REST APIs", 96, True, 3, cat_backend.id),
            ("Node.js", 85, True, 4, cat_backend.id),
            ("Three.js", 82, False, 5, cat_backend.id),
            ("Socket.IO", 84, False, 6, cat_backend.id),
            # Databases
            ("MySQL", 92, True, 1, cat_db.id),
            ("MongoDB", 88, True, 2, cat_db.id),
            ("PostgreSQL", 86, True, 3, cat_db.id),
            ("AWS", 80, False, 4, cat_db.id),
            ("Docker", 82, False, 5, cat_db.id),
            # Architecture
            ("Object-Oriented Design (OOP)", 95, True, 1, cat_arch.id),
            ("Data Structures & Algorithms", 90, True, 2, cat_arch.id),
            ("Role-Based Access Control (RBAC)", 94, True, 3, cat_arch.id),
            ("Git & GitHub", 95, False, 4, cat_arch.id),
            ("Postman API Testing", 92, False, 5, cat_arch.id),
            ("Linux & Bash", 85, False, 6, cat_arch.id)
        ]
        for name, prof, feat, ord_num, c_id in skills_data:
            db.add(Skill(name=name, proficiency=prof, featured=feat, order=ord_num, category_id=c_id))

        # Seed Projects
        proj1 = Project(
            slug="attendance-management-system",
            title="Attendance Management System",
            tagline="Automated QR Code & Geofencing Attendance Architecture",
            description="Production web application engineered with Python, Flask, HTML5, CSS3, and JavaScript featuring automated QR scanning and GPS geofence verification.",
            content="""# Attendance Management System
Engineered a production-grade automated attendance solution to eliminate manual errors and proxy logging.

### Architecture Highlights:
- **Haversine Geofencing Engine**: Enforces exact GPS coordinate radii around authorized campus coordinates.
- **Dynamic QR Code Tokens**: Ephemeral QR tokens expiring every 60 seconds to prevent replay attacks.
- **Role-Based Access Control**: Multi-tier permissions across Student, Instructor, and Campus Administrator portals.
- **Export Pipelines**: Automated generation of PDF & Excel attendance logs for administrative auditing.
""",
            cover_image="/portrait-cutout.png",
            category="Full Stack",
            technologies=json.dumps(["Python", "Flask", "JavaScript", "HTML5", "CSS3", "MySQL", "Geofencing", "QR Codes"]),
            metrics=json.dumps({"Accuracy": "99.8%", "Scan Latency": "<200ms", "Daily Active Users": "1,200+"}),
            github_url="https://github.com/shashidharpc/attendance-management-system",
            featured=True,
            published=True,
            order=1,
            views_count=384
        )

        proj2 = Project(
            slug="wheelz-vehicle-rental-system",
            title="Wheelz — Vehicle Rental System",
            tagline="Multi-tier vehicle booking platform with automated billing",
            description="Comprehensive vehicle rental application built with PHP, MySQL, and JavaScript, handling fleet management and booking workflows.",
            content="""# Wheelz Vehicle Rental System
Comprehensive rental management platform built with PHP and relational MySQL schemas.

### Key Capabilities:
- **Relational Booking Architecture**: Handles conflict-free vehicle availability calendars.
- **Automated Billing Engine**: Dynamically calculates rental rates, insurance tiers, and late penalty adjustments.
- **Customer Portal**: Self-service vehicle selection, booking confirmation, and digital invoicing.
""",
            cover_image="/portrait-cutout.png",
            category="Full Stack",
            technologies=json.dumps(["PHP", "MySQL", "JavaScript", "HTML5", "CSS3", "Bootstrap"]),
            metrics=json.dumps({"Fleet Capacity": "500+ Vehicles", "Query Response": "<120ms", "Booking Efficiency": "+45%"}),
            github_url="https://github.com/shashidharpc/wheelz-vehicle-rental",
            featured=True,
            published=True,
            order=2,
            views_count=215
        )
        db.add_all([proj1, proj2])

        # Seed Experience & Education
        exp1 = Experience(
            role="Full Stack Software Engineer",
            company="Independent Software Projects & Applied Research",
            location="Bengaluru, India",
            period="2024 — Present",
            description="Developing end-to-end full stack web platforms, REST APIs, and automated telemetry systems.",
            achievements=json.dumps([
                "Architected and deployed an automated attendance management system using Python, Flask, and GPS geofencing.",
                "Engineered multi-tier vehicle rental system with PHP and MySQL relational schemas.",
                "Designed and implemented RESTful APIs with strict Role-Based Access Control (RBAC)."
            ]),
            technologies=json.dumps(["Python", "Flask", "JavaScript", "PHP", "MySQL", "MongoDB", "REST APIs", "Git"]),
            order=1,
            current=True
        )

        exp2 = Experience(
            role="Master of Computer Applications (MCA)",
            company="Presidency College",
            location="Bengaluru, Karnataka",
            period="2022 — 2024",
            description="Postgraduate coursework focused on Advanced Software Engineering, Cloud Architecture, Algorithms, and Distributed Computing.",
            achievements=json.dumps([
                "Graduated with 8.75 CGPA.",
                "Specialized in full-stack web platforms and database architectures."
            ]),
            technologies=json.dumps(["Algorithms", "System Design", "Cloud Computing", "Database Management"]),
            order=2,
            current=False
        )

        exp3 = Experience(
            role="Bachelor of Computer Applications (BCA)",
            company="Sahyadri Science College",
            location="Kuvempu University",
            period="2019 — 2022",
            description="Undergraduate foundation in Computer Science, Data Structures, OOP, and Database Management Systems.",
            achievements=json.dumps([
                "Graduated with Distinction: 89.86% aggregate score.",
                "Core coursework: C, Java, Python, Web Fundamentals, Software Engineering."
            ]),
            technologies=json.dumps(["Data Structures", "OOP", "DBMS", "Software Engineering"]),
            order=3,
            current=False
        )
        db.add_all([exp1, exp2, exp3])

        # Seed Geofence Zone
        zone = GeofenceZone(
            name="Bengaluru Tech Campus",
            latitude=12.9716,
            longitude=77.5946,
            radius_meters=300.0,
            is_active=True
        )
        db.add(zone)

        db.commit()
        print("Database seeding completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
