"""This file is to update the created Database"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sports_database import Categories, Base, LatestItem, User

engine = create_engine('sqlite:///sports_database.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(id=1, name="Aadit Bhojgi", email="aaditbhojgi@gmail.com",
             picture='https://scontent-sin6-2.xx.fbcdn.net/v/t1.0-9/'
                     '17309870_1370861142937308_2632912282125339192_n'
                     '.jpg?oh=fed0551a43c2638c46aaa56b5206ac88&oe=59DD17E1')
session.add(User1)
session.commit()

# Items for Soccer
sports1 = Categories(user_id=1, name="Soccer",
                     description_cat="Association football, more commonly "
                                     "known as football or soccer, is a "
                                     "team sport played between two teams of "
                                     "eleven players with a spherical ball. "
                                     "It is played by 250 million players in "
                                     "over 200 countries and dependencies, "
                                     "making it the world's most popular "
                                     "sport.The game is played on a "
                                     "rectangular field "
                                     "with a goal at each end. The object "
                                     "of the"
                                     " game is to score by getting the "
                                     "ball into "
                                     "the opposing goal. ")

session.add(sports1)
session.commit()

sportItem1 = LatestItem(user_id=1, title="Soccer Ball",
                        description="A football, soccer ball, or "
                                    "association "
                                    "football ball is the ball used in "
                                    "the sport "
                                    "of association football. The name "
                                    "of the ball "
                                    "varies according to whether the "
                                    "sport is called "
                                    "'football', 'soccer', or 'association"
                                    " football'. "
                                    "The ball's spherical shape, as well"
                                    " as its size, "
                                    "weight, and material composition, "
                                    "are specified by "
                                    "Law 2 of the Laws of the Game "
                                    "maintained by the "
                                    "International Football Association"
                                    " Board. Additional,"
                                    " more stringent, standards are "
                                    "specified by FIFA and "
                                    "subordinate governing bodies for the"
                                    " balls used in "
                                    "the competitions they sanction.",
                        item_category=sports1.name, categories=sports1)

session.add(sportItem1)
session.commit()

sportItem2 = LatestItem(user_id=1, title="Soccer Jersey",
                        description="In association football, kit "
                                    "(also referred to as strip"
                                    " or soccer uniform) is the standard"
                                    " equipment and attire "
                                    "worn by players. The sport's Laws "
                                    "of the Game specify the "
                                    "minimum kit which a player must use,"
                                    " and also prohibit the "
                                    "use of anything that is dangerous "
                                    "to either the player or "
                                    "another participant. Individual "
                                    "competitions may stipulate "
                                    "further restrictions, such as regulating"
                                    " the size of logos "
                                    "displayed on shirts and stating that,"
                                    " in the event of a match "
                                    "between teams with identical or "
                                    "similar colours, the away "
                                    "team must change to different coloured"
                                    " attire.",
                        item_category=sports1.name, categories=sports1)

session.add(sportItem2)
session.commit()

sportItem3 = LatestItem(user_id=1, title="Soccer Cleats",
                        description="Football boots, called cleats or "
                                    "soccer shoes in North "
                                    "America, are an item of footwear "
                                    "worn when playing football. "
                                    "Those designed for grass pitches "
                                    "have studs on the outsole to"
                                    " aid grip. From simple and humble"
                                    " beginnings football boots "
                                    "have come a long way and today find"
                                    " themselves subject to "
                                    "much research, development, "
                                    "sponsorship and marketing at "
                                    "the heart of a multi-national global"
                                    " industry. Modern "
                                    "'boots' are not truly boots in that"
                                    " they do not cover "
                                    "the ankle - like most other types "
                                    "of specialist sports "
                                    "footwear, their basic design and "
                                    "appearance has converged "
                                    "with that of sneakers since the 1960s.",
                        item_category=sports1.name, categories=sports1)

session.add(sportItem3)
session.commit()

# Items for Basketball
sports2 = Categories(user_id=1, name="Basketball",
                     description_cat="Basketball is a non-contact sport"
                                     " played on a "
                                     "rectangular court. While most "
                                     "often played as "
                                     "a team sport with five players on"
                                     " each side, "
                                     "three-on-three, two-on-two, and"
                                     " one-on-one "
                                     "competitions are also common. "
                                     "The objective "
                                     "is to shoot a ball through a hoop"
                                     " 18 inches "
                                     "(46 cm) in diameter and 10 feet"
                                     " (3.048 m) high"
                                     " that is mounted to a backboard"
                                     " at each end of "
                                     "the court. The game was invented"
                                     " in 1891 by "
                                     "Dr. James Naismith, who would be"
                                     " the first "
                                     "basketball coach of the Kansas"
                                     " Jayhawks, "
                                     "one of the most successful "
                                     "programs in the game's history.")

session.add(sports2)
session.commit()

sportItem4 = LatestItem(user_id=1, title="Basketball (ball)",
                        description="A basketball is a spherical inflated"
                                    " ball used in basketball"
                                    " games. Basketballs typically range"
                                    " in size from very small"
                                    " promotional items only a few inches"
                                    " in diameter to extra "
                                    "large balls nearly a foot in diameter"
                                    " used in training exercises."
                                    " For example, a basketball in high "
                                    "school would be about 27 inches"
                                    " in circumference, while an NBA ball "
                                    "would be about 29 inches. "
                                    "The actual standard size of a "
                                    "basketball in the NBA is 29.5 inches"
                                    " in circumference.",
                        item_category=sports2.name, categories=sports2)

session.add(sportItem4)
session.commit()

sportItem5 = LatestItem(user_id=1, title="Basketball Jersey",
                        description="A basketball uniform is a type of"
                                    " uniform worn by basketball "
                                    "players. Basketball uniforms "
                                    "consist of a jersey that features "
                                    "the number and last name of the "
                                    "player on the back, as well as "
                                    "shorts and athletic shoes. Within"
                                    " teams, players wear uniforms "
                                    "representing the team colors; the"
                                    " home team typically wears a "
                                    "lighter-colored uniform, while "
                                    "the visiting team wears a "
                                    "darker-colored uniform.",
                        item_category=sports2.name, categories=sports2)

session.add(sportItem5)
session.commit()

sportItem6 = LatestItem(user_id=1, title="Basketball Shoes",
                        description="In 1903, a special basketball"
                                    " shoe with suction cups to "
                                    "prevent slippage was added to"
                                    " the official basketball uniform"
                                    " demonstrated in the Spalding"
                                    " catalog. Over the decades, different"
                                    " shoe brands and styles were popular"
                                    " as basketball shoes: Chuck Taylor"
                                    " All-Stars and Keds in the 1960s"
                                    " and 70s; Adidas and Nike leather "
                                    "high-tops in the late 1970s and"
                                    " 80s; and Air Jordans in the 1990s.",
                        item_category=sports2.name, categories=sports2)

session.add(sportItem6)
session.commit()

# Items for Baseball
sports3 = Categories(user_id=1, name="Baseball",
                     description_cat="Baseball is a bat-and-ball game"
                                     " played between two teams of "
                                     "nine players each, who take "
                                     "turns batting and fielding."
                                     "The batting team attempts to"
                                     " score runs by hitting a ball"
                                     " that is thrown by the pitcher"
                                     " with a bat swung by the batter,"
                                     " then running counter-clockwise"
                                     " around a series of four bases:"
                                     " first, second, third, and home"
                                     " plate. A run is scored when a"
                                     " player advances around the bases"
                                     " and returns to home plate.")

session.add(sports3)
session.commit()

sportItem7 = LatestItem(user_id=1, title="Baseball Bat",
                        description="A baseball bat is a smooth wooden"
                                    " or metal club used in the "
                                    "sport of baseball to hit the ball"
                                    " after it is thrown by the "
                                    "pitcher. By regulation it may be"
                                    " no more than 2.75 inches "
                                    "(70 mm) in diameter at the "
                                    "thickest part and no more than 42 "
                                    "inches (1,100 mm) long. Although"
                                    " historically bats approaching "
                                    "3 pounds (1.4 kg) were swung,[1]"
                                    " today bats of 33 ounces (0.94 kg)"
                                    " are common, topping out at 34"
                                    " ounces (0.96 kg) to 36 "
                                    "ounces (1.0 kg).",
                        item_category=sports3.name, categories=sports3)

session.add(sportItem7)
session.commit()

sportItem8 = LatestItem(user_id=1, title="Baseball (ball)",
                        description="A baseball is a ball used in"
                                    " the sport of the same name,"
                                    " baseball."
                                    " The ball features a rubber"
                                    " or cork center, wrapped in"
                                    " yarn, and"
                                    " covered, in the words of"
                                    " the Official Baseball "
                                    "Rules: with two "
                                    "strips of white horsehide"
                                    " or cowhide, tightly "
                                    "stitched together. ",
                        item_category=sports3.name, categories=sports3)

session.add(sportItem8)
session.commit()

# Items for Frisbee
sports4 = Categories(user_id=1, name="Frisbee",
                     description_cat="Flying disc games are"
                                     " games played with discs,"
                                     " often called by the"
                                     " trademarked name Frisbees."
                                     " Ultimate and disc golf"
                                     " are sports with"
                                     " substantial international"
                                     " followings")

session.add(sports4)
session.commit()

sportItem9 = LatestItem(user_id=1, title="Frisbee Disc",
                        description="A frisbee (also called a"
                                    " flying disc or simply a"
                                    " disc) is a gliding"
                                    " toy or sporting item that"
                                    " is generally plastic and"
                                    " roughly 20 to 25"
                                    " centimetres (8 to 10 in)"
                                    " in diameter with a lip,"
                                    " used recreationally"
                                    " and competitively for "
                                    "throwing and catching,"
                                    " for example, in flying"
                                    " disc games. The shape"
                                    " of the disc, an airfoil"
                                    " in cross-section, allows"
                                    " it to fly by generating"
                                    " lift as it moves through"
                                    " the air while spinning.",
                        item_category=sports4.name, categories=sports4)

session.add(sportItem9)
session.commit()

# Items for Snowboarding
sports5 = Categories(user_id=1, name="Snowboarding",
                     description_cat="Flying disc games are"
                                     " games played with discs,"
                                     " often called by the"
                                     " trademarked name Frisbees."
                                     " Ultimate and disc golf"
                                     " are sports with"
                                     " substantial international"
                                     " followings")

session.add(sports5)
session.commit()

sportItem10 = LatestItem(user_id=1, title="Goggles",
                         description="Ski goggles are goggles"
                                     " that help protect a skiers"
                                     " eyes from the sun.",
                         item_category=sports5.name, categories=sports5)

session.add(sportItem10)
session.commit()

sportItem11 = LatestItem(user_id=1, title="Snowboard",
                         description="Snowboards are boards that"
                                     " are usually the width of"
                                     " one's foot longways, with"
                                     " the ability to glide on"
                                     " snow."
                                     " Snowboards are "
                                     "differentiated from"
                                     " monoskis by the stance"
                                     " of the user. In "
                                     "monoskiing, the user "
                                     "stands with feet inline"
                                     " with direction of "
                                     "travel (facing tip of"
                                     " monoski/downhill)"
                                     " (parallel to long axis"
                                     " of board), whereas in"
                                     " snowboarding,"
                                     " users stand with feet"
                                     " transverse (more or less)"
                                     " to the "
                                     "longitude of the board."
                                     " Users of such equipment"
                                     " may be referred"
                                     " to as snowboarders. "
                                     "Commercial snowboards "
                                     "generally require"
                                     " extra equipment such as"
                                     " bindings and special boots"
                                     " which help"
                                     " secure both feet of a "
                                     "snowboarder, who generally"
                                     " rides in an"
                                     " upright position. These "
                                     "types of boards are "
                                     "commonly used by"
                                     " people at ski hills or"
                                     " resorts for leisure, "
                                     "entertainment,"
                                     " and competitive purposes"
                                     " in the activity called"
                                     " snowboarding.",
                         item_category=sports5.name, categories=sports5)

session.add(sportItem11)
session.commit()

# Items for Rock climbing
sports6 = Categories(user_id=1, name="Rock Climbing",
                     description_cat="Rock climbing is an activity"
                                     " in which participants climb up,"
                                     " down or across natural rock"
                                     " formations or artificial rock"
                                     " walls."
                                     " The goal is to reach the "
                                     "summit of a formation or the"
                                     " endpoint of"
                                     " a usually pre-defined route"
                                     " without falling. Due to the"
                                     " length and"
                                     " extended endurance required"
                                     " and because accidents are "
                                     "more likely to"
                                     " happen on the descent than"
                                     " the ascent, rock climbers"
                                     " do not usually"
                                     " climb back down the route.")

session.add(sports6)
session.commit()

sportItem12 = LatestItem(user_id=1, title="Rope and Webbing",
                         description="Climbing ropes are typically"
                                     " of kernmantle construction, "
                                     "consisting of a core (kern)"
                                     " of long twisted fibres and an "
                                     "outer sheath (mantle) of woven"
                                     " coloured fibres. The core "
                                     "provides about 80% of the "
                                     "tensile strength, while the "
                                     "sheath"
                                     " is a durable layer that "
                                     "protects the core and gives"
                                     " the rope"
                                     " desirable handling "
                                     "characteristics.",
                         item_category=sports6.name, categories=sports6)

session.add(sportItem12)
session.commit()

sportItem13 = LatestItem(user_id=1, title="Helmet",
                         description="The climbing helmet is a"
                                     " piece of safety equipment "
                                     "that "
                                     "primarily protects the skull"
                                     " against falling debris "
                                     "(such as rocks or dropped "
                                     "pieces of protection) and "
                                     "impact"
                                     " forces during a fall. ",
                         item_category=sports6.name, categories=sports6)

session.add(sportItem13)
session.commit()

sportItem14 = LatestItem(user_id=1, title="Climbing Shoes",
                         description="Specifically designed"
                                     " foot wear is usually"
                                     " worn for "
                                     "climbing. To increase"
                                     " the grip of the foot"
                                     " on a climbing"
                                     " wall or rock face due"
                                     " to friction, the shoe"
                                     " is soled"
                                     " with a vulcanized rubber"
                                     " layer. Usually, shoes are"
                                     " only"
                                     " a few millimetres thick"
                                     " and fit very snugly "
                                     "around the foot.",
                         item_category=sports6.name, categories=sports6)

session.add(sportItem14)
session.commit()

# Items for Foosball
sports7 = Categories(user_id=1, name="Foosball",
                     description_cat="To begin the game, the ball"
                                     " is served through a hole"
                                     " at the side of the table,"
                                     " or simply placed by hand at"
                                     " the feet of a figure in "
                                     "the centre of the table."
                                     " The initial serving side"
                                     " is decided with a coin toss."
                                     " Players attempt to use "
                                     "figures mounted on rotating"
                                     " bars"
                                     " to kick the ball into the"
                                     " opposing goal. Expert players"
                                     " have been known to move "
                                     "balls at speeds up to 56 km/h"
                                     " (35 mph) in competition")

session.add(sports7)
session.commit()

sportItem15 = LatestItem(user_id=1, title="Foosball Table",
                         description="Climbing ropes are typically"
                                     " of kernmantle construction, "
                                     "consisting of a core (kern)"
                                     " of long twisted fibres and"
                                     " an "
                                     "outer sheath (mantle) of "
                                     "woven coloured fibres. The"
                                     " core "
                                     "provides about 80% of the"
                                     " tensile strength, while"
                                     " the sheath"
                                     " is a durable layer that"
                                     " protects the core and "
                                     "gives the rope"
                                     " desirable handling"
                                     " characteristics.",
                         item_category=sports7.name, categories=sports7)

session.add(sportItem15)
session.commit()

# Items for Skating
sports8 = Categories(user_id=1, name="Skating",
                     description_cat="Skating involves any"
                                     " sports or recreational"
                                     " activity"
                                     " which consists of "
                                     "traveling on surfaces"
                                     " or on ice using skates.")

session.add(sports8)
session.commit()

sportItem16 = LatestItem(user_id=1, title="Skates",
                         description="Roller skating is the"
                                     " traveling on surfaces"
                                     " with"
                                     " roller skates. It is a"
                                     " form of recreational activity"
                                     " as well as a sport, and"
                                     " can also be a form of"
                                     " transportation. Skates"
                                     " generally come in three"
                                     " basic varieties: quad "
                                     "roller skates, inline skates"
                                     " or blades and tri-skates,"
                                     " though some have"
                                     " experimented with a "
                                     "single-wheeled"
                                     " 'quintessence skate' or other"
                                     " variations"
                                     " on the basic skate design. ",
                         item_category=sports8.name, categories=sports8)

session.add(sportItem16)
session.commit()

sportItem17 = LatestItem(user_id=1, title="Helmet and Protective Gears",
                         description="Protects skater "
                                     "from injuries caused by"
                                     " accidents.",
                         item_category=sports8.name, categories=sports8)

session.add(sportItem17)
session.commit()

# Items for Hockey
sports9 = Categories(user_id=1, name="Hockey",
                     description_cat="Hockey is a sport in"
                                     " which two teams"
                                     " play against each"
                                     " other by trying to"
                                     " maneuver a ball or"
                                     " a puck into the"
                                     " opponent's goal "
                                     "using a hockey stick."
                                     " There are many types"
                                     " of hockey such as"
                                     " bandy, field hockey"
                                     " and ice hockey")

session.add(sports9)
session.commit()

sportItem18 = LatestItem(user_id=1, title="Hockey Stick",
                         description="A hockey stick is a"
                                     " piece of equipment"
                                     " used by the players"
                                     " in most forms of"
                                     " hockey to move the"
                                     " ball or puck.",
                         item_category=sports9.name, categories=sports9)

session.add(sportItem18)
session.commit()

sportItem19 = LatestItem(user_id=1, title="Hockey Ball",
                         description="The core of the ball is"
                                     " made of"
                                     " cork and this is surrounded"
                                     " by rubber or rubber-like"
                                     " plastic."
                                     "The ball should be manufactured"
                                     " in a diameter of 62.4 mm or"
                                     "63.8 mm (the latter is called"
                                     " 'Russian ball') and the colour"
                                     " was originally red, later "
                                     "orange or cerise."
                                     " According to the Bandy"
                                     " Playing Rules set up by the"
                                     " Federation of International"
                                     " Bandy, any of these is"
                                     " allowed, but all balls used"
                                     " in one game must be of"
                                     " the same colour and type.",
                         item_category=sports9.name, categories=sports9)

session.add(sportItem19)
session.commit()

sportItem20 = LatestItem(user_id=1, title="Hockey Jersey",
                         description="Hockey sweaters today"
                                     " are typically"
                                     " made of tough synthetic"
                                     " materials"
                                     " like polyester, to help"
                                     " take away"
                                     " moisture and keep the "
                                     "wearer dry. In"
                                     " accordance with the "
                                     "team's colors and"
                                     " matching the socks, "
                                     "they are usually"
                                     " emblazoned with the "
                                     "team's logo on the"
                                     " front, the player's "
                                     "last name on the upper back",
                         item_category=sports9.name, categories=sports9)

session.add(sportItem20)
session.commit()

print 'Nice, Database Populated!'
