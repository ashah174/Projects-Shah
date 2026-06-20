const express = require("express");
const router = express.Router();
const Itinerary = require("../models/Itinerary");

// GET all itineraries
router.get("/", async (req, res) => {
  try {
    const itineraries = await Itinerary.find().sort({ createdAt: -1 });
    res.json(itineraries);
  } catch (error) {
    res.status(500).json({ message: "Error getting itineraries", error });
  }
});

// GET public itineraries
router.get("/public", async (req, res) => {
  try {
    const itineraries = await Itinerary.find({ isPublic: true }).sort({
      createdAt: -1,
    });

    res.json(itineraries);
  } catch (error) {
    res.status(500).json({ message: "Error fetching public itineraries" });
  }
});

// GET search results
router.get("/search", async (req, res) => {
  try {
    const { destination } = req.query;

    const itineraries = await Itinerary.find({
      destination: { $regex: destination || "", $options: "i" },
    });

    res.json(itineraries);
  } catch (error) {
    res.status(500).json({ message: "Error searching itineraries", error });
  }
});

// GET one itinerary
router.get("/:id", async (req, res) => {
  try {
    const itinerary = await Itinerary.findById(req.params.id);

    if (!itinerary) {
      return res.status(404).json({ message: "Itinerary not found" });
    }

    res.json(itinerary);
  } catch (error) {
    res.status(500).json({ message: "Error getting itinerary", error });
  }
});

// CREATE itinerary
router.post("/", async (req, res) => {
  try {
    const newItinerary = new Itinerary(req.body);
    const savedItinerary = await newItinerary.save();
    res.status(201).json(savedItinerary);
  } catch (error) {
    res.status(400).json({ message: "Error creating itinerary", error });
  }
});

// UPDATE itinerary
router.put("/:id", async (req, res) => {
  try {
    const updatedItinerary = await Itinerary.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );

    res.json(updatedItinerary);
  } catch (error) {
    res.status(500).json({ message: "Error updating itinerary", error });
  }
});

// DELETE itinerary
router.delete("/:id", async (req, res) => {
  try {
    await Itinerary.findByIdAndDelete(req.params.id);
    res.json({ message: "Itinerary deleted" });
  } catch (error) {
    res.status(500).json({ message: "Error deleting itinerary", error });
  }
});

router.post("/:id/comments", async (req, res) => {
  try {
    const { rating, text, username } = req.body;

    const itinerary = await Itinerary.findById(req.params.id);

    if (!itinerary) {
      return res.status(404).json({ message: "Itinerary not found" });
    }

    itinerary.comments.push({
      username: username || "Anonymous",
      rating,
      text,
      date: new Date(),
    });

    await itinerary.save();

    res.json(itinerary);
  } catch (error) {
    res.status(500).json({ message: "Error adding comment", error });
  }
});

router.put("/:id/comments/:commentId", async (req, res) => {
  try {
    const { rating, text } = req.body;

    const itinerary = await Itinerary.findById(req.params.id);
    if (!itinerary) {
      return res.status(404).json({ message: "Itinerary not found" });
    }

    const comment = itinerary.comments.id(req.params.commentId);
    if (!comment) {
      return res.status(404).json({ message: "Comment not found" });
    }

    comment.rating = rating;
    comment.text = text;

    await itinerary.save();
    res.json(itinerary);
  } catch (error) {
    res.status(500).json({ message: "Error updating comment", error });
  }
});

router.delete("/:id/comments/:commentId", async (req, res) => {
  try {
    const itinerary = await Itinerary.findById(req.params.id);
    if (!itinerary) {
      return res.status(404).json({ message: "Itinerary not found" });
    }

    itinerary.comments.pull(req.params.commentId);

    await itinerary.save();
    res.json(itinerary);
  } catch (error) {
    res.status(500).json({ message: "Error deleting comment", error });
  }
});

module.exports = router;