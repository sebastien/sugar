;;; sugar-mode.el --- major mode for Sugar code

;; Copyright (C) 2007 Akoha, Inc.

;; Author: Simon Law <simon@akoha.org>
;; Created: 2007/08/31
;; Revised: 2007/09/04
;; Keywords: font-lock emacs-lisp sugar

;; sugar-mode is free software; you can redistribute it and/or modify
;; it under the terms of the GNU Lesser General Public License as
;; published by the Free Software Foundation; either version 2, or (at
;; your option) any later version.

;; sugar-mode is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU Lesser General Public
;; License along with sugar-mode; see the file COPYING.  If not, write
;; to the Free Software Foundation, Inc., 51 Franklin Street, Fifth
;; Floor, Boston, MA 02110-1301, USA.

;;; Commentary:

;; sugar-mode is a major mode to support the Sugar meta-programming
;; language <http://www.ivy.fr/sugar/>.
;;
;; To enable it, add it to your Emacs path this to your ~/.emacs file:
;;
;;     (autoload 'sugar-mode "/path/to/sugar-mode.el"
;;        "Major mode for editing Sugar files" t)
;;     (setq auto-mode-alist (cons '("\\.sjs$" . sugar-mode) auto-mode-alist))


;;; Code:

(defvar sugar-mode-map
  (let ((sugar-mode-map (make-keymap)))
    (define-key sugar-mode-map "\C-j" 'sugar-newline-and-indent)
    sugar-mode-map)
  "Keymap for Sugar major mode")

(defvar sugar-font-lock-defaults
  (list '("^\\s-*|[^\"\n]*"
	  . font-lock-doc-face)
	'("\\(?:@\\<\\(?:c\\(?:lass\\|onstructor\\)\\|end\\|function\\|m\\(?:ethod\\|odule\\)\\|property\\|shared\\|target\\|version\\)\\|\\<\\(?:a\\(?:nd\\|s\\)\\|break\\|c\\(?:atch\\|ontinue\\)\\|e\\(?:lse\\|nd\\)\\|f\\(?:inally\\|or\\)\\|has\\|i[fns]\\|n\\(?:ew\\|ot\\)\\|or\\|r\\(?:aise\\|eturn\\)\\|try\\|var\\|while\\|yield\\)\\)\\>"
	  . font-lock-keyword-face)
	'("\\<\\(?:true\\|false\\|null\\|self\\)\\>"
	  . font-lock-constant-face))
  "Font-lock defaults for Sugar mode")

(defvar sugar-mode-syntax-table
  (let ((sugar-mode-syntax-table (make-syntax-table)))
    (modify-syntax-entry ?_ "w" sugar-mode-syntax-table)
    (modify-syntax-entry ?# "<" sugar-mode-syntax-table)
    (modify-syntax-entry ?\n ">" sugar-mode-syntax-table)
    sugar-mode-syntax-table)
  "Syntax table for Sugar mode")

(defconst sugar-indent-regexp "\\(?:^\\s-*\\(?:@\\<\\(?:c\\(?:lass\\|onstructor\\)\\|end\\|function\\|method\\)\\|\\<\\(?:catch\\|else\\|f\\(?:or\\|inally\\)\\|if\\|try\\|while\\)\\)\\>\\|.*{[^{}]*$\\)"
  "Regexp that matches lines that open blocks")
(defconst sugar-unindent-regexp "\\(?:^\\s-*@?end\\|.*}[^{]*$\\)"
  "Regexp that matches lines that close blocks")

(defun sugar-indent-line ()
  "Indent current line as Sugar code"
  (interactive)
  (beginning-of-line)
  (if (bobp)
      (indent-line-to 0)
    (let ((not-indented t)
	  cur-indent)
      (if (looking-at sugar-unindent-regexp)
	  (save-excursion
	    (while not-indented
	      (forward-line -1)
	      (if (looking-at sugar-indent-regexp)
		  (progn
		    (setq cur-indent (current-indentation))
		    (setq not-indented nil))
		(if (looking-at sugar-unindent-regexp)
		    (progn
		      (setq cur-indent (- (current-indentation) default-tab-width))
		      (setq not-indented nil))
		  (if (bobp)
		      (setq not-indented nil)))))
	      (if (< cur-indent 0)
		  (setq cur-indent 0)))
	(save-excursion
	  (while not-indented
	    (forward-line -1)
	    (if (looking-at sugar-unindent-regexp)
		(progn
		  (setq cur-indent (current-indentation))
		  (setq not-indented nil))
	      (if (looking-at sugar-indent-regexp)
		  (progn
		    (setq cur-indent (+ (current-indentation) default-tab-width))
		    (setq not-indented nil))
		(if (bobp)
		    (setq not-indented nil)))))))
      (if cur-indent
	  (indent-line-to cur-indent)
	(indent-line-to 0)))))

(defun sugar-newline-and-indent ()
  "Reindent current line, insert newline, then indent the new line."
  (interactive "*")
  (let ((pos (point)))
    (newline)
    (save-excursion
      (goto-char pos)
      (indent-according-to-mode))
    (indent-according-to-mode)))

(define-derived-mode sugar-mode fundamental-mode "Sugar"
  "Major mode to edit Sugar files."
  (set (make-local-variable 'comment-start) "# ")
  (set (make-local-variable 'comment-start-skip) "#+\\s-*")
  (set (make-local-variable 'font-lock-defaults) '(sugar-font-lock-defaults))
  (set (make-local-variable 'indent-line-function) 'sugar-indent-line))

(provide 'sugar-mode)
