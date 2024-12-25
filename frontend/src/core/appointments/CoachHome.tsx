import { useUser } from "@context/UserContext";

const CoachHome: React.FC = () => {
    const { user } = useUser();
    return (
        <div>
            <h1>Coach Home</h1>
            <p>Welcome, {user?.username}!</p>
        </div>
    );
};

export default CoachHome;