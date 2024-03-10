// Function to open the popup
function openPopup(nodeName) {

    document.getElementById("popupOverlay").style.display = "block";
}

// Function to close the popup
function closePopup() {
    document.getElementById("popupOverlay").style.display = "none";
}

function textPopup(index) {
    var popup = document.getElementById("myPopup");
    // popup.innerText="Welcome to Studytonight"; 
    popup.innerText= texts[index]
    // popup.classList.toggle("show");
    window.open("#container", "_self");
}

function createPopup(index){
    var popup = open("", "Popup", "width=500,height=300");
    var aOk = popup.document.createElement("p");
    aOk.innerHTML = texts[index]
    popup.document.body.appendChild(aOk);
    }
    

var texts = [
    "We invite you to join the Flutter team, which is made up of volunteers and sponsored folk alike! There are many ways to contribute, including writing code, filing issues on GitHub, helping people on our mailing lists, our chat channels, or on Stack Overflow, helping to triage, reproduce, or fix bugs that people have filed, adding to our documentation, doing outreach about Flutter, or helping out in any other way.We grant commit access (which includes full rights to the issue database, such as being able to edit labels) to people who have gained our trust and demonstrated a commitment to Flutter. For more details see the Contributor access page on our wiki.We communicate primarily over GitHub and Discord.Before you get started, we encourage you to read these documents which describe some of our community norms: Our code of conduct, which stipulates explicitly that everyone must be gracious, respectful, and professional. This also documents our conflict resolution policy and encourages people to ask questions.Values, which talks about what we care most about."
    , 'Triage is the process of going through bug reports and determining if they are valid, finding out how to reproduce them, catching duplicate reports, and generally making our issues list useful for our engineers.\
    If you want to help us triage, you are very welcome to do so!\
    Join the #hackers-triage Discord channel.\
    Read our code of conduct, which stipulates explicitly that everyone must be gracious, respectful, and professional. If you\'re helping out with triage, you are representing the Flutter team, and so you want to make sure to make a good impression!\
    Help out as described in our wiki: https://github.com/flutter/flutter/wiki/Triage You won\'t be able to add labels at first, so instead start by trying to do the other steps, e.g. trying to reproduce the problem and asking for people to provide enough details that you can reproduce the problem, pointing out duplicates, and so on. Chat on the #hackers-triage channel to let us know what you\'re up to!\
    Familiarize yourself with our issue hygiene wiki page, which covers the meanings of some important GitHub labels and milestones.\
    Once you\'ve been doing this for a while, someone will invite you to the flutter-hackers team on GitHub and you\'ll be able to add labels too. See the contributor access wiki page for details.'
    ,
    'The Flutter team uses a Discord server, which you are invited to join. The server is open to the public, though some channels are intended only for people who are actively contributing. See the #welcome channel for instructions on posting to the server (you won\'t be able to see the channels until you acknowledge the rules there).\
    We recommend you use the same display name on Discord and GitHub.\
    (Our Flutter Discord server is unrelated to the r/FlutterDev Discord server, which is where the r/FlutterDev community shares their apps, discusses Flutter, and so on. When in doubt, remember: our server has Dash as an icon.)'
    ,
    'To triage an issue, first look at the bug report, and try to understand what the described problem is. Edit the original comment to remove boilerplate that the bug reporter didn\'t remove. Edit the original comment to add backticks (```) around blocks of stack traces, code, the output of shell scripts like flutter doctor, etc. Ensure that the title is a meaningful summary of the issue. These changes make the bug much easier to manage.\
    If their report is unclear, doesn\'t give sufficient steps to reproduce, or is otherwise lacking in sufficient detail for us to act on it, add a polite comment asking for additional information, add the waiting for customer response label, then skip the remaining steps.\
    If the bug is still unclear -- we have previously asked for more detail, and the bug reporter has had a chance to provide additional feedback, but has not been able to do so in a way that makes the bug actionable -- either apologize for us not being able to fix it and then close the bug, or add the waiting for customer response label, depending on your confidence that the reporter will be able to eventually provide sufficient detail. \
    Then, skip the remaining steps. It is fine to be aggressive in closing bugs where the issue is not clear, because we have plenty of other issues where the bug is clear and there\'s really no value to us in having low-quality bugs open in our bug database.\
    If the issue describes something that you know for a fact has been fixed since the bug report was filed, add a cheerful comment saying so, close the issue, and skip the remaining steps.\
    If the bug is clear enough for us to act on it, continue with the following steps. To reach this step, the bug should be actionable, with clear steps to reproduce the problem. We have enough bugs filed that we will not run out of work any time soon; therefore, \
    it is reasonable to be quite aggressive in establishing if a bug is sufficiently clear.'
    ,
    'An actionable issue is one for which it is easy to determine if a particular PR means the issue can be closed or not. Issues whose descriptions are vague, or that express a general malaise or general desire, issues that specify a failure mode but no steps to reproduce the problem, and other issues where the nature of the problem is not clear and where it would be difficult to determine if any particular change could actually fix the problem, should be closed.\
    One example of an unactionable issue is one with such vaguely described symptoms that lots of people claim to have the same problem even when their described situations differ in mutually exclusive ways.\
    As a project with literally thousands of open issues, we are not lacking in feedback. Time that would be spent trying to understand an unclear issue could be more effectively spent on a bug with a clear description. \
    Unactionable bugs are simply not valuable enough to keep around when we have many actionable bugs already. Indeed, given how such issues are likely to affect search results, \
    confuse new users filing issues, or attract hostile comments due to remaining open for a long time, they may literally have a negative value to the project.\
    ',
    'If you recognize that this bug is a duplicate of an existing bug, add a reference to that bug in a comment, then close the bug. Skip the remaining steps. As you triage more and more bugs you will become more and more familiar with the existing bugs and so you will get better and better at marking duplicates in this way.\
    When closing the duplicate bug, the github issue tracker does not copy the list of people being notified on the closed bug into the original bug. This can matter, especially when asking on the original bug for things like reproduction steps. Consider cc\'ing the author of the duplicate issue into the original issue,\
     especially if we\'re still trying to determine reproduction steps for the issue.'
     ,

]