import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Activity from './pages/Activity';

export default function Routes() {
    return (
        <BrowserRouter>
            <Switch>
                <Route path="/" exact component={Activity} />
            </Switch>
        </BrowserRouter>
    );
}