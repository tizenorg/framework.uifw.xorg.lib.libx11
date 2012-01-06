/*

Copyright 1986, 1998  The Open Group

Permission to use, copy, modify, distribute, and sell this software and its
documentation for any purpose is hereby granted without fee, provided that
the above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation.

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of The Open Group shall not be
used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization from The Open Group.

*/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
#ifdef _F_ENABLE_XI2_SENDEVENT_
#include <X11/extensions/geproto.h>
#endif//_F_ENABLE_XI2_SENDEVENT_
#include "Xlibint.h"

/*
 * In order to avoid all images requiring _XEventToWire, we install the
 * event converter here if it has never been installed.
 */
Status
XSendEvent(
    register Display *dpy,
    Window w,
    Bool propagate,
    long event_mask,
    XEvent *event)
{
#ifdef _F_ENABLE_XI2_SENDEVENT_
    Status status;

    LockDisplay (dpy);

    /* call through display to find proper conversion routine */

    if (event->type == GenericEvent) {
        static Bool ext_initialized = False;
        static _XExtension *ext = NULL;
        XGenericEventCookie *xcookie = (XGenericEventCookie *) event;
        xGenericEvent *ev = NULL;
        register Status (**fp)(
            Display *            /* dpy */,
            XGenericEventCookie* /* re */,
            xGenericEvent **     /* event */);

        if (!ext_initialized) {
            for (ext = dpy->ext_procs; ext; ext = ext->next) {
                if (ext->name && strcmp (ext->name, GE_NAME) == 0)
                    break;
            }

            ext_initialized = True;
        }

        /* No XGE */
        if (!ext)
            return BadRequest;

        fp = &dpy->generic_wire_vec[xcookie->extension & 0x7F];

        if (!fp || !*fp)
            return BadRequest;

        status = (**fp)(dpy, xcookie, &ev);

        if (status && ev) {
            register xGESendEventReq *req;
            register long len;

            GetReq (GESendEvent, req);

            req->reqType = ext->codes.major_opcode;
            req->ReqType = X_GESendEvent;
            req->destination = w;
            req->propagate = propagate;
            req->eventMask = event_mask;

            len = ev->length;
            len += SIZEOF (xEvent) >> 2;

            if (dpy->bigreq_size || req->length + len <= (unsigned) 65535) {
                SetReqLen(req, len, len);
                Data (dpy, (char *)ev, len << 2);
            } else {
                XFree(ev);
                return BadLength;
            }
        }

        if (ev)
            XFree(ev);
    } else {
        xEvent ev;
        register Status (**fp)(
            Display *       /* dpy */,
            XEvent *        /* re */,
            xEvent *        /* event */);

        /* initialize all of the event's fields first, before setting
         * the meaningful ones later.
         */
        memset (&ev, 0, sizeof (ev));

        fp = &dpy->wire_vec[event->type & 0177];
        if (*fp == NULL) *fp = _XEventToWire;
        status = (**fp)(dpy, event, &ev);

        if (status) {
            register xSendEventReq *req;

            GetReq(SendEvent, req);
            req->destination = w;
            req->propagate = propagate;
            req->eventMask = event_mask;
#ifdef WORD64
            /* avoid quad-alignment problems */
            memcpy ((char *) req->eventdata, (char *) &ev, SIZEOF(xEvent));
#else
            req->event = ev;
#endif /* WORD64 */
        }
    }
#else//_F_ENABLE_XI2_SENDEVENT_
    register xSendEventReq *req;
    xEvent ev;
    register Status (**fp)(
                Display *       /* dpy */,
                XEvent *        /* re */,
                xEvent *        /* event */);
    Status status;

    /* initialize all of the event's fields first, before setting
     * the meaningful ones later.
     */
    memset (&ev, 0, sizeof (ev));

    LockDisplay (dpy);

    /* call through display to find proper conversion routine */

    fp = &dpy->wire_vec[event->type & 0177];
    if (*fp == NULL) *fp = _XEventToWire;
    status = (**fp)(dpy, event, &ev);

    if (status) {
	GetReq(SendEvent, req);
	req->destination = w;
	req->propagate = propagate;
	req->eventMask = event_mask;
#ifdef WORD64
	/* avoid quad-alignment problems */
	memcpy ((char *) req->eventdata, (char *) &ev, SIZEOF(xEvent));
#else
	req->event = ev;
#endif /* WORD64 */
    }
#endif//_F_ENABLE_XI2_SENDEVENT_

    UnlockDisplay(dpy);
    SyncHandle();
    return(status);
}
