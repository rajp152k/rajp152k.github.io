---
title: "Pragmatic Opacity"
date: 2025-10-05T18:03:33+05:30
categories: ["Emacs"]
tags: ["emacs","UI","UX","productivity"]
draft: false
---

---
{{<youtube "nimOCOiBXsA">}}
---

This video explores a productivity workflow in Emacs that leverages window opacity, moving it beyond a purely aesthetic feature. The creator demonstrates how a translucent Emacs frame can be used as an overlay to view and control background applications, improving efficiency and saving screen real estate.

### The Concept of Functional Opacity

*   [00:00:12] The creator initially viewed opacity as just for aesthetics but accidentally discovered a practical use case.
*   [00:01:46] The core idea is to *decouple focus from control*. The user can remain focused within Emacs while their controls are passed through to a background application.
*   [00:02:09] To achieve this, granular opacity controls have been set up with convenient key bindings, allowing for interactive adjustments or quick toggling between preset levels (e.g., low, medium, high).

### Practical Demonstration: Emacs and Org-roam UI

*   [00:02:58] The primary use case shown is with Org-roam notes. The Emacs window is made translucent, revealing the Org-roam UI graph visualization running in a Chromium browser window behind it.
*   [00:03:55] Thanks to Org-roam UI's "follow mode," which uses WebSockets, the creator can navigate their notes in Emacs, and the graph in the background browser automatically updates to follow their position.
*   [00:04:25] All control over the background graph (e.g., switching from a local to a global view) is done from within Emacs using key bindings, eliminating the need to `alt-tab` or switch windows.
*   [00:06:51] This method improves productivity by allowing the user to view related visual information (the graph) while working on text (the notes) in the same screen space, without splitting windows or using multiple monitors.

### Expanding the Idea: Decoupling Focus and Control

*   [00:05:32] The creator notes that the current Org-roam setup is tightly coupled. The long-term vision is for a more generic system.
*   [00:05:54] The ideal setup would be a general "bypass" mode where controls from Emacs could be sent to *any* background application (e.g., scrolling a webpage in Firefox) while the user remains in their editor.
*   [00:06:34] This concept might require development at the window manager or compositor level to properly manage which application receives input, regardless of which one is visually in focus.

### Related Personalizations and Future Ideas

*   [00:08:41] The creator mentions purchasing split foot pedals to add more input methods without causing repetitive strain injury ("ankle RSI").
*   [00:09:28] There's an interest in exploring `Emacs Live` and `Overtone`, a musical synthesizer, to create music based on keystrokes and chords while typing.

### Conclusion

[00:10:11] The video serves as a demonstration of the creator's evolving philosophy on user interfaces. The goal is to find more efficient, productive, and fun ways to interact with the computer. By reimagining a simple feature like opacity, a novel workflow emerges that saves time and screen space, representing an *emergent pattern* from years of "messing around" with system configurations.
