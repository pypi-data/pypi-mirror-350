/** @odoo-module **/
import '@mail/models/activity_box_view';
import { registerPatch } from '@mail/model/model_core';

registerPatch({
    name: 'ActivityBoxView',
    fields: {
        activityViews: many('ActivityView', {
            compute() {
                return this.chatter.thread.activities.filter(activity => activity.state != "done").map(activity => {
                    return { activity };
                });
            },
            inverse: 'activityBoxView',
        }),
    }
});

