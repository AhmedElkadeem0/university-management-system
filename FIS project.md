db.instructors.insertMany(\[

  {

    employee\_id: 1001,

    first\_name: "Mostafa",

    last\_name: "Soliman",

    department: "Computer Science",

    salary: 120000.00,

    courses\_taught: \["CS401", "CS305"]

  },

  {

    employee\_id: 1002,

    first\_name: "Ayman",

    last\_name: "Arafa",

    department: "Mathematics",

    salary: 95000.00,

    courses\_taught: \["MA201", "MA101"]

  },

  {

    employee\_id: 1003,

    first\_name: "Hassan",

    last\_name: "Shokry",

    department: "Physics",

    salary: 105000.00,

    courses\_taught: \["PH200"]

  },

  {

    employee\_id: 1004,

    first\_name: "Amal",

    last\_name: "Gomaa",

    department: "Business",

    salary: 115000.00,

    courses\_taught: \["BUS310", "BUS400"]

  },

  {

    employee\_id: 1005,

    first\_name: "Reda",

    last\_name: "Basiouny",

    department: "Computer Science",

    salary: 88000.00,

    courses\_taught: \["CS101"]

  }

])







// First, get all the instructor IDs

var MostafaId = db.instructors.findOne({employee\_id: 1001}).\_id;

var AymanId = db.instructors.findOne({employee\_id: 1002}).\_id;

var HassanId = db.instructors.findOne({employee\_id: 1003}).\_id;

var AmalId = db.instructors.findOne({employee\_id: 1004}).\_id;

var RedaId = db.instructors.findOne({employee\_id: 1005}).\_id;



// Then insert courses with the variables

db.courses.insertMany(\[

  {

    course\_code: "CS101",

    title: "Intro to Programming",

    description: "Fundamentals of software development.",

    credit\_hours: 3,

    instructor\_id: MostafaId

  },

  {

    course\_code: "MA101",

    title: "Calculus I",

    description: "Limits, derivatives, and integration.",

    credit\_hours: 4,

    instructor\_id: AymanId

  },

  {

    course\_code: "CS401",

    title: "Advanced Database Systems",

    description: "Non-relational databases and distributed systems.",

    credit\_hours: 3,

    instructor\_id: RedaId

  },

  {

    course\_code: "BUS310",

    title: "Marketing Principles",

    description: "Core concepts of modern marketing.",

    credit\_hours: 3,

    instructor\_id: AmalId

  },

  {

    course\_code: "PH200",

    title: "Classical Mechanics",

    description: "Newtonian physics and dynamics.",

    credit\_hours: 4,

    instructor\_id: HassanId

  },

  {

    course\_code: "CS305",

    title: "Data Structures",

    description: "Arrays, lists, trees, and graphs.",

    credit\_hours: 3,

    instructor\_id: RedaId

  },

  {

    course\_code: "MA201",

    title: "Linear Algebra",

    description: "Vectors, matrices, and linear transformations.",

    credit\_hours: 3,

    instructor\_id: AymanId

  },

  {

    course\_code: "BUS400",

    title: "Financial Accounting",

    description: "Principles of financial reporting.",

    credit\_hours: 3,

    instructor\_id: AmalId

  }

])













db.students.insertMany(\[

  {

    student\_id: 320230052,

    first\_name: "Ahmed",

    last\_name: "Elkadeem",

    email: "ahmed.320230052@ejust.edu.eg",

    enrollment\_date: new Date("2023-09-01"),

    gpa: 3.85,

    is\_active: true,

    courses\_enrolled: \["CS101", "MA101", "PH200"]

  },

  {

    student\_id: 320230014,

    first\_name: "jana",

    last\_name: "yousri",

    email: "jana.320230014@ejust.edu.eg",

    enrollment\_date: new Date("2023-09-01"),

    gpa: 3.70,

    is\_active: true,

    courses\_enrolled: \["CS101", "BUS310"]

  },

  {

    student\_id: 320230109,

    first\_name: "omar",

    last\_name: "negm",

    email: "omar.320230109@ejust.edu.eg",

    enrollment\_date: new Date("2023-09-05"),

    gpa: 4.00,

    is\_active: true,

    courses\_enrolled: \["CS401", "CS305", "MA201"]

  },

  {

    student\_id: 320230044,

    first\_name: "omar",

    last\_name: "dorgham",

    email: "omar.320230044@ejust.edu.eg",

    enrollment\_date: new Date("2023-09-05"),

    gpa: 2.95,

    is\_active: true,

    courses\_enrolled: \["BUS310", "BUS400"]

  },

  {

    student\_id: 320230051,

    first\_name: "nasser",

    last\_name: "hossam",

    email: "nasser.320230051@ejust.edu.eg",

    enrollment\_date: new Date("2023-09-15"),

    gpa: 3.55,

    is\_active: true,

    courses\_enrolled: \["MA101", "PH200"]

  },

  {

    student\_id: 320230050,

    first\_name: "ahmed",

    last\_name: "tahan",

    email: "ahmed.320230050@ejust.edu.eg",

    enrollment\_date: new Date("2023-09-10"),

    gpa: 2.50,

    is\_active: true,

    courses\_enrolled: \["CS401", "BUS400"]

  },

  {

    student\_id: 320230033,

    first\_name: "eyad",

    last\_name: "ahmed",

    email: "eyad.320230033@ejust.edu.eg",

    enrollment\_date: new Date("2022-09-10"),

    gpa: 3.90,

    is\_active: true,

    courses\_enrolled: \["CS305", "MA201", "PH200"]

  },

  {

    student\_id: 320230057,

    first\_name: "ahmed",

    last\_name: "maher",

    email: "ahmed.320230057@ejust.edu.eg",

    enrollment\_date: new Date("2024-09-01"),

    gpa: 3.20,

    is\_active: true,

    courses\_enrolled: \["CS101"]

  },

  {

    student\_id: 320230062,

    first\_name: "mariem",

    last\_name: "tamer",

    email: "mariem.320230062@ejust.edu.eg",

    enrollment\_date: new Date("2021-09-15"),

    gpa: 3.75,

    is\_active: false, // Inactive student

    courses\_enrolled: \[]

  },

  {

    student\_id: 320230077,

    first\_name: "heba",

    last\_name: "zahran",

    email: "heba.320230077@ejust.edu.eg",

    enrollment\_date: new Date("2023-09-05"),

    gpa: 3.30,

    is\_active: true,

    courses\_enrolled: \["MA101", "BUS310", "BUS400"]

  }

])







db.students.insertOne({

  student\_id: 320230099,

  first\_name: "malak",

  last\_name: "osama",

  email: "malak.320230099@ejust.edu.eg",

  enrollment\_date: new Date(),

  gpa: 0.00,

  is\_active: true,

  courses\_enrolled: \[]

})







db.students.find()

db.students.find({ gpa: { $gt: 3.5 } })

db.students.find({ courses\_enrolled: "CS101" })

db.students.find().sort({ gpa: -1 })

db.students.find({}, { first\_name: 1, last\_name: 1, email: 1, gpa: 1, \_id: 0 })

db.students.find().skip(5).limit(5)



db.students.updateOne(

  { student\_id: 320230109 },

  { $set: { gpa: 3.88, is\_active: false } }

)



db.students.updateOne(

  { student\_id: 320230044 },

  { $unset: { is\_active: "" } }

)



db.students.updateOne(

  { student\_id: 320230014 },

  { $inc: { gpa: 0.1 } }

)



db.students.updateOne(

  { student\_id: 320230062 },

  { $rename: { "email": "contact\_email" } }

)



db.students.updateOne(

  { student\_id: 320230052 },

  { $push: { courses\_enrolled: "MA201" } }

)



db.students.updateOne(

  { student\_id: 320230052 },

  { $pull: { courses\_enrolled: "MA201" } }

)



db.students.updateOne(

  { student\_id: 320230052 },

  { $addToSet: { courses\_enrolled: "MA201" } }

)



db.students.updateOne(

  { student\_id: 320230044 },

  { $mul: { gpa: 1.05 } }

)



db.students.updateOne(

  { student\_id: 320230052 },

  { $min: { gpa: 4.00 } }

)





db.students.deleteOne({ first\_name: "mariem", last\_name: "tamer" })



db.students.deleteMany({ enrollment\_date: { $lt: new Date("2023-01-01") } })



db.courses.updateOne(

  { course\_code: "CS101" },

  { $set: { credit\_hours: 4 } }

)



db.courses.deleteOne({ title: "Classical Mechanics" })



db.instructors.updateOne(

  { employee\_id: 1001 },

  { $mul: { salary: 1.10 } }

)



db.instructors.updateOne(

  { employee\_id: 1003 },

  { $push: { courses\_taught: "PH100" } }

)



db.instructors.updateOne(

  { employee\_id: 1003 },

  { $pull: { courses\_taught: "PH200" } }

)



db.instructors.updateOne(

  { employee\_id: 1004 },

  { $rename: { "department": "dept" } }

)



db.instructors.deleteOne({ employee\_id: 1005 })





# ATLAS

db.students.insertOne({

  student\_id: 320230052,

  first\_name: "Ahmed",

  last\_name: "Elkadeem",

  email: "ahmed.320230052@ejust.edu.eg",

  enrollment\_date: new Date(),

  gpa: 3.85,

  is\_active: true,

  courses\_enrolled: \["MA101"]

})



db.students.find({ first\_name: "Ahmed" })





db.students.updateOne(

  { first\_name: "Ahmed" },

  { $set: { gpa: 3.50 } }

)



db.students.deleteOne({ first\_name: "Ahmed" })

