from syncer import db, models

d = models.Device("9830958175928574")
d.name, d.password, d.number, d.protocol = "Batmobile", "123666", "9995559955", "gps103"
db.session.add(d)
d = models.Device("9364850374387564")
d.name, d.password, d.number, d.protocol = "Invisible Jet", "112233", "9911223344", "gps103"
db.session.add(d)
d = models.Device("6473957689023837")
d.name, d.password, d.number, d.protocol = "Batwing", "654321", "9191919191", "gt06"
db.session.add(d)
d = models.Device("9583658703785934")
d.name, d.password, d.number, d.protocol = "Kent Pickup", "123456", "9999900000", "gt02"
db.session.add(d)
d = models.Device("8493760217587697")
d.name, d.password, d.number, d.protocol = "F-22 Raptor", "123456", "9876512345", "gps103"
db.session.add(d)
d = models.Device("666666666666666")
d.name, d.password, d.number, d.protocol = "Getaway Vehicle II", "658743", "9847563746", "gps103"
db.session.add(d)
d = models.Device("4476846566587697")
d.name, d.password, d.number, d.protocol = "Batstrike", "654333", "9292929292", "gt02"
db.session.add(d)
d = models.Device("5487820577665980")
d.name, d.password, d.number, d.protocol = "Bike IV", "000000", "8379589834", "gps103"
db.session.add(d)
d = models.Device("8876376590235475")
d.name, d.password, d.number, d.protocol = "LadyBird", "456123", "8768769090", "gt02"
db.session.add(d)
d = models.Device("7823465456536278")
d.name, d.password, d.number, d.protocol = "Rolls Royce Wayne Edition", "123456", "8383839292", "gps103"
db.session.add(d)
d = models.Device("8876376590754246")
d.name, d.password, d.number, d.protocol = "Shelby Super Snake", "839201", "8769089090", "gt02"
db.session.add(d)
d = models.Device("666622666666666")
d.name, d.password, d.number, d.protocol = "Joker's Joyride", "None", "67584923", "gt06"
db.session.add(d)
db.session.commit()

u = models.User("bruce@wayne.tech")
u.name, u.password = "Bruce Wayne", "batman"
u.devices.append(models.Device.query.get("9830958175928574"))
u.devices.append(models.Device.query.get("6473957689023837"))
u.devices.append(models.Device.query.get("4476846566587697"))
db.session.add(u)
u = models.User("ww@jla.org")
u.name, u.password = "Diana Prince", "amz"
u.devices.append(models.Device.query.get("9364850374387564"))
db.session.add(u)
u = models.User("jordan@ferrisair.com")
u.name, u.password = "Hal Jordan", "nofear"
u.devices.append(models.Device.query.get("8493760217587697"))
db.session.add(u)
u = models.User("barry.allen@ccpd.gov")
u.name, u.password = "Barry Allen", "iris"
db.session.add(u)
u = models.User("joker4u@4chan.com")
u.name, u.password = "Nemo", "jngcsaf76234hjf"
u.devices.append(models.Device.query.get("666666666666666"))
db.session.add(u)
u = models.User("ckent@dailyplanet.com")
u.name, u.password = "Clark Kent", "momdad"
u.devices.append(models.Device.query.get("9583658703785934"))
db.session.add(u)
u = models.User("t.drake@gotham.edu")
u.name, u.password = "Tim Drake", "wolfman89"
u.devices.append(models.Device.query.get("9830958175928574"))
u.devices.append(models.Device.query.get("7823465456536278"))
db.session.add(u)
u = models.User("gray@cio.us")
u.name, u.password = "Dick Grayson", "bludhaven"
u.devices.append(models.Device.query.get("7823465456536278"))
u.devices.append(models.Device.query.get("5487820577665980"))
u.devices.append(models.Device.query.get("9830958175928574"))
db.session.add(u)
u = models.User("alfred@wayne.org")
u.name, u.password = "Alfred Pennyworth", "bruce"
u.devices.append(models.Device.query.get("7823465456536278"))
db.session.add(u)
u = models.User("orkl@anon.net")
u.name, u.password = "Barbara Gordon", "Err0r4O4"
db.session.add(u)
u = models.User("get@huntress.com")
u.name, u.password = "Helena Rosa Bertinelli", "helenahuntresshelenahuntress"
u.devices.append(models.Device.query.get("8876376590235475"))
db.session.add(u)
u = models.User("penguin@rspca.org")
u.name, u.password = "Oswald Chesterfield Cobblepot", "antart1ca"
db.session.add(u)
u = models.User("ceo@lex.corp")
u.name, u.password = "Lex Luthor", "krypt0nite"
db.session.add(u)
u = models.User("Muri")
u.name, u.password = "None", "None"
db.session.add(u)
u = models.User("mache")
u.name, u.password = "None", "None"
db.session.add(u)
db.session.commit()

