#!/bin/zsh
# /fast stages 4-6: cut -> faces -> cards -> render -> audio -> preview + FCPXML -> stills -> DTD check -> open in FCP.
# Usage: run.sh <slug e.g. img1805-rpn> [stills seconds ...]. Prints a timestamp per stage.
set -e
SLUG=$1; shift; NUM=${SLUG//[^0-9]/}
KIT=${0:A:h}; REPO=${FAST_RPN_REPO:-${KIT:h:h:h:h}}   # repo root = 4 levels up from .claude/skills/fast-rpn/kit
[[ -d $REPO/videos ]] || REPO="$HOME/Developer/personal edit/video-edit-fonts-styles"
R="$REPO/videos/$SLUG"; G="$HOME/Movies/FCP/$SLUG-graphics"; V=~/.cache/fast-rpn/venv/bin/python
DTD=${FCPXML_DTD:-$HOME/.cache/fast-rpn/FCPXMLv1_14.dtd}   # copied from Final Cut Pro.app/Contents/Frameworks/Interchange.framework/.../Resources (xmllint chokes on the spaces)
cd "$R/scripts"
st() { echo "== $(date +%T) $1"; }
st cut;    $V cut.py
st faces;  $V faces.py
st cards;  $V assets.py
st render; $V build.py main all
st audio;  $V audio.py main
st finish; $V finish.py main all
cp "$R/renders/main/img${NUM}_rpn_preview.mp4" "$G/img${NUM}_rpn_final.mp4"
st stills; $V stills.py main ${@:-2.0 5.0 20.0}
st check;  xmllint --noout --dtdvalid "$DTD" "$G/img${NUM}_rpn.fcpxml" && echo "DTD OK"
[[ -z $NO_OPEN ]] && open -a "Final Cut Pro" "$G/img${NUM}_rpn.fcpxml"
st done
