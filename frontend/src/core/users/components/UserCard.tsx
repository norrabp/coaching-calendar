import React from 'react';
import { normalizePhone } from '@util/normalize-phone-number';
import { toTitleCase } from '@util/string-format';

interface IUser {
    id: number;
    username: string;
    email: string;
    phone_number: string;
    role: string;
}

const UserCard: React.FC<{user: IUser}> = ({user}) => {
    console.log(user);
    return (
        <div key={user.id} className="col-md-4 mb-3">
            <div className="card bg-dark">
                <div className="card-body">
                <h5 className="card-title">{user.username}</h5>
                <p className="card-text">{toTitleCase(user.role)}</p>
                <p className="card-text text-muted">{user.email}</p>
                <p className="card-text">
                    <small className="text-muted">{normalizePhone(user.phone_number)}</small>
                </p>
                </div>
            </div>
        </div>
    )
}

export default UserCard;