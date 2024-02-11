
# HTTP2Ser

Experimental program to provide a text view of a web page on a dumb terminal or
computer running a serial terminal.

Expected terminal types are: ANSI, VT-102, VT-52, ADM-3A, and PETSCII terminals. 

Web pages must be formatted using compatible HTML tags. This allows the pages to
be visible on PC web browsers, as well. 

* `<text>`: blocks, if present, will display text verbatim. If any `<text>`
  blocks are present, body text outside of `<text>` blocks will not be displayed.
  Depending on the user's terminal type, only one of these blocks will be
  displayed. 
    * The **type** attribute can be used to filter terminal types. So text
      inside of `<term type="ansi,vt102">` will only display on ANSI and VT-102
      terminals. This allows you to craft screens for specific display types.
    * Text will will be rendered as Code Page 437, aka ANSI or IBM Extended
      ASCII.
* HTML Entities as seen on
  [w3schools](https://www.w3schools.com/html/html_entities.asp) will be
  converted to their ASCII equivalents. 
    * `&nbsp;`: renders as 
    * `&lt;` : \< symbol
    * `&gt;` \> symbol
    * `&apos;` \' symbol
* additional escape codes are defined for terminal use:  
    * `\r` (13 or $0d): move the cursor to the start of a line. Does *not*
      advance the cursor to the next line.
    * `\n` (10 or $0A): moves the cursor to the next line on the first column.
      When needed, this sends a CR and LF bytes to the terminal.
    * `\[` (27 or $1b). Send the ESC byte.
    * `\xFF` transmit a byte value.
    * `\\` transmit the backslash.
* `<br/>` sends a newline sequence
* `<p>` and `</p>` starts and ends a paragraph. The terminal will skip a line
  after the closing tag.
* `<a>` tags should have a **key** attribute. Pressing this key will follow that
    hyperlink. **Key** can be a hex or entity code. Example:
    `<ahref="post.php&forum=3" key="N">New Message</a>`
* `<span>` tags with style information will be converted to 
* Special tags for cursor position and color
    * `<pos x=n y=n />` tags will position the cursor at a place on the screen.
      X and Y are 1-based
    * `<color fg=n bg=n rvs=y|n/>` sets the foreground and background color.
        * fg and bg 0-15 will be mapped to the ANSI color code for ANSi modes. For PETSCII mode, the value is transmitted as-is.
        * rvs swaps the last foreground and background colors or sets RVS ON or RVS OFF for PETSCII terminals.
    * `<home />` moves the cursor to the top left corner of the screen.
    * `<clear />` clears the screen
* Form input: the user can move between form fiels with the arrow up/down keys,
  the tab key, or the Enter/Return key. Input fields should be *outside* of `<term>` blocks, and any prompts placed using the term block text.
    * `<input id="id" type=text x=n y=n width=n />` presents a single text field.
    * `<input id="id" type=check x=n y=n value="yes" />` presents a Y/n field.
      If the **checked** attribute is present, the default will be Y. Otherwise,
      the default is N.
    * `<input id="id" type=textarea x=n y=n width=n height=n />` presents a text
      field with an editor. If the terminal allows, a full screen editor will be presented. Pressing ESC twice will break out of the editor and return to the page view (with the edited text on screen.)
    * `<input id="id" type="select">...` pressing Enter when this field is
      highlighted will show a list of items on the screen. Typing directly into the field will present a type-ahead text field using the `<option>` values.    
    * `<input id="id" type="submit" key="X" />` pressing the defined key submits
      the form.
* Menus: use `<a>` tags to create menu prompts. To encode  
  `[R]eply [N]ext [M]enu [Q]uit` 
  as a one-line prompt, use `<a>` tags:
  ```
  <a href="reply.php" key="R">Reply</a>
  <a href="reply.php" key="R">Reply</a>

  ```