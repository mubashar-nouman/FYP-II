function getBotResponse(input) {
    // Simple responses
    if (input == "hello" || input == "Hello") {
        return "Hello there!";
    }
    else if (input == "goodbye" || input == "Goodbye"){
        return "Talk to you later!";
    }
    else if (input == "I am feeling fever"){
        return "Take some medicine! I hope you will get well soon!";
    }
    else if (input == "I love UET!"){
        return "I love UET too!";
    }
    else {
        return "Try asking something else!";
    }
}